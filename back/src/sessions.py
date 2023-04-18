from src.database import connection
from src.configuration import options
from src.edusign import EdusignToken
from operator import itemgetter
from typing import Any
import datetime
import Yawaei
import asyncio
import aiohttp
import heapq
import itertools

def update_student(login, status, session_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    if status == 'present':
        status = 'present'
    else:
        status = 'NULL'
    t = f"""
        UPDATE student SET status=%s WHERE session_id=%s and login=%s
    """

    try:
        cursor.execute(t, (status, session_id, login))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True

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

def get_database_session(event_id):
    cursor = connection.cursor()
    t = f"""
        SELECT * from session WHERE id={event_id}
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

def get_any_student_name(entry: dict[str, Any]) -> str | None:
    return entry.get('EMAIL', entry.get('login', None))

def late_student_zipper(all_students, late_entries):
    all_students = sorted(all_students, key=itemgetter('EMAIL'))
    late_entries = sorted(late_entries, key=itemgetter('login'))
    queue = heapq.merge(all_students, late_entries, key=get_any_student_name)

    for login, values in itertools.groupby(queue, get_any_student_name):
        result = dict(map(lambda p: (p[1], p[0].get(p[1], None)), zip(values, ('ID', 'delay'))))
        if result.get('delay', None) is not None and result.get('ID', None) is not None:
            yield result

def get_students_ids(edusign_students, intra_students):
    present_students = [a['login'] for a in intra_students 
        if a['status'] == 'present']

    late_students = [{
        'login': a['login'], 
        'delay': abs(divmod((datetime.datetime.strptime(options.late_limit, '%H:%M:%S') 
        - datetime.datetime.strptime(a['late'], '%H:%M:%S')).total_seconds(), 60)[0])} 
        for a in intra_students if a['late'] != 'NULL']

    late_login = [a['login'] for a in late_students if a['delay'] < options.maximum_late_time]

    present_students = present_students + late_login

    ids = [a['ID'] for a in edusign_students if a['EMAIL'] in present_students]
    late_ids = late_student_zipper(edusign_students, late_students)

    return ids, list(late_ids)

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

async def sign_single_school(edusign, date, session_index):
    sessions = await edusign.get_sessions(date)
    if not sessions:
        return None

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
        try:
            edusign_students = await edusign.get_students(to_sign_session['edusign_id'])
        except KeyError:
            continue
        ids, late_ids = get_students_ids(edusign_students, intra_students+remote_students)
        sign = await edusign.sign_session(to_sign_session['edusign_id'])
        mail = await edusign.send_mails(ids, to_sign_session['edusign_id'])
        if not mail.get('result') == 'mail already sent':
            late = await edusign.send_lates(late_ids, to_sign_session['edusign_id'])
        print(sign, mail)

async def sign_all_sessions(date, session_index):
    """Sign all sessions
    """
    edusign = EdusignToken()
    for cred in options.all_edusign_credentials:
        school_ids = await edusign.login(cred['login'], cred['password'])
        for school_id, token in list(school_ids.items()):
            edusign.set_school_id(school_id)
            edusign.set_token(token)
            await sign_single_school(edusign, date, session_index)

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
    for cred in options.all_edusign_credentials:
        school_ids = await edusign.login(cred['login'], cred['password'])
        sessions = []
        for school_id, token in list(school_ids.items()):
            edusign.set_school_id(school_id)
            edusign.set_token(token)
            school_session = await edusign.get_sessions(session_date)
            sessions += school_session

        if not sessions:
            raise SessionNotAvailableException(f'No session available for the date {session_date}')

        choices = [min(sessions, key=lambda x: x['end']), max(sessions, key=lambda x: x['begin'])]
        session_hour = choices[session_index]['begin' if session_index == 0 else 'end'][11:-1]

        database_session = get_database_event_by_date(session_date, session_hour)
        if database_session:
            raise SessionAlreadyCreated(f'Session already created for the date {session_date} and hour {session_hour}')

        session_id = create_session(session_date, session_hour)
        session_hour = convert_time_utc_local_intra(f'{session_date} {session_hour}')

        intra_session = Intra.get_events(
            options.event_activity,
            date=session_date,
            hour=session_hour
        )
        students = Intra.get_registered_students(options.event_activity + intra_session[0])
        for student in students.keys():
            add_student(student, students[student], session_id)

async def refresh_session(session_id):
    Intra = Yawaei.intranet.AutologinIntranet(f'auth-{options.intranet_secret}')
    res = get_database_session(session_id)
    if len(res) != 1:
        raise KeyError('Session not found')
    session_date = res[0]['date']
    session_hour = res[0]['hour']
    session_hour = convert_time_utc_local_intra(f'{session_date} {session_hour}')

    intra_session = Intra.get_events(
        options.event_activity,
        date=session_date,
        hour=session_hour
    )

    students = Intra.get_registered_students(options.event_activity + intra_session[0])

    database_students = get_database_student(session_id)    
    for student in students.keys():
        current_student = list(filter(lambda x: x['login'] == student, database_students))
        if current_student[0]['late'] == 'NULL' or current_student[0]['late'] == None:
            update_student(student, students[student], session_id)