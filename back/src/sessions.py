from src.database import connection
from src.configuration import options
from src.edusign import EdusignToken
import datetime
import Yawaei
import asyncio
import aiohttp

def get_database_event_by_date(date, hour):
    cursor = connection.cursor()
    t = f"""
        SELECT * from session WHERE date="{date}" and hour="{hour}"
    """
    try:
        cursor.execute(t)
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def get_database_student(event_id):
    cursor = connection.cursor()
    t = f"""
        SELECT * from student WHERE session_id={event_id}
    """
    try:
        cursor.execute(t)
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def get_remote_student(date):
    cursor = connection.cursor()
    t = f"""
        SELECT * from remote
    """
    try:
        cursor.execute(t)
        res = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    result = [{**a, 'status': 'present', 'late': 'NULL'} for a in res if a['begin'] < date and a['end'] > date]
    return result

#TODO: Envoyer les retard séparément des présences (retard edusign)
def get_students_ids(edusign_students, intra_students):
    present_students = [a['login'] for a in intra_students 
        if a['status'] == 'present' or (a['late'] != 'NULL' and a['late'] < options.late_limit)]
    late_ids = [{'login': a['login'], 'delay': 
        divmod((datetime.datetime.strptime(options.late_limit, '%H:%M:%S') 
        - datetime.datetime.strptime(a['late'], '%H:%M:%S')).total_seconds(), 60)[0]} 
        for a in intra_students if a['late'] != 'NULL' and a['late'] < options.late_limit]
    ids = [a['ID'] for a in edusign_students if a['EMAIL'] in present_students]
    return ids, late_ids

class BaseCustomException(Exception):
    pass

class SessionNotCreatedException(BaseCustomException):
    pass

class SessionNotValidatedException(BaseCustomException):
    pass

class SessionNotAvailableException(BaseCustomException):
    pass

class SessionAlreadyCreated(BaseCustomException):
    pass

async def sign_all_sessions(date, session_index):
    """Sign all sessions
    """
    edusign = EdusignToken()
    await edusign.login()
    sessions = await edusign.get_sessions(date)
    if not sessions:
        raise SessionNotAvailableException(f'No session available for the date {date}')
    choices = [min(sessions, key=lambda x: x['end']), max(sessions, key=lambda x: x['begin'])]
    hour = choices[session_index]['begin' if session_index == 0 else 'end'][11:-1]

    database_session = get_database_event_by_date(date, hour)
    if not database_session:
        raise SessionNotCreatedException("Database session not created")

    if database_session[0]['is_approved'] == 0:
        raise SessionNotValidatedException("Session need validation")

    intra_students = get_database_student(str(database_session[0]['id']))
    remote_students = get_remote_student(date)
    edusign_sessions = await edusign.get_sessions(date)
    to_sign_sessions = [e for e in edusign_sessions if e['begin'][11:-1] == hour or e['end'][11:-1] == hour]

    for to_sign_session in to_sign_sessions:
        edusign_students = await edusign.get_students(to_sign_session['edusign_id'])
        ids, late_ids = get_students_ids(edusign_students, intra_students+remote_students)
        sign = await edusign.sign_session(to_sign_session['edusign_id'])
        mail = await edusign.send_mails(ids, to_sign_session['edusign_id'])
        # TODO: Create a lateness function which emit late report for every late_ids ({'login': "", 'delay': "1"})

def create_session(date, hour, is_approved=False):
    cursor = connection.cursor()
    t = f"""
        INSERT INTO session (date, hour, is_approved)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(t, (date, hour, is_approved))
    except Exception as e:
        print('Error with sql : ', e)
        return False
    connection.commit()
    return cursor.lastrowid

def add_student(login, status, session_id):
    cursor = connection.cursor()
    t = f"""
        INSERT INTO student (login, status, session_id)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(t, (login, status, session_id))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True

def convert_time_utc_local_intra(iso_date):
    date = datetime.datetime.fromisoformat(iso_date)
    return (date + options.timezone.utcoffset(date)).strftime('%H:00')

async def create_single_session(session_date, session_index):
    """Create a session : fetch students, create db session and create students attendance entries
    """
    Intra = Yawaei.intranet.AutologinIntranet(f'auth-{options.intranet_secret}')

    edusign = EdusignToken()
    await edusign.login()

    sessions = await edusign.get_sessions(session_date)

    if not sessions:
        raise SessionNotAvailableException(f'No session available for the date {session_date}')

    choices = [min(sessions, key=lambda x: x['end']), max(sessions, key=lambda x: x['begin'])]
    session_hour = choices[session_index]['begin' if session_index == 0 else 'end'][11:-1]
    session_id = create_session(session_date, session_hour)
    session_hour = convert_time_utc_local_intra(f'{session_date} {session_hour}')

    database_session = get_database_event_by_date(session_date, session_hour)
    if database_session:
        raise SessionAlreadyCreated(f'Session already created for the date {session_date} and hour {session_hour}')

    intra_session = Intra.get_events(
        options.event_activity,
        date=session_date,
        hour=session_hour
    )
    students = Intra.get_registered_students(options.event_activity + intra_session[0])
    for student in students.keys():
        add_student(student, students[student], session_id)