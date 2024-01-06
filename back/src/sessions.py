from src.crud.student_session import add_student_session, read_student_session, update_student_session_from_intra
from src.crud.student import  read_student
from src.crud.session import get_session_by_date, read_session, create_session
from src.crud.remote import get_remote_by_date
from src.crud.week_plan import get_weekplan
from src.database import connection
from src.configuration import options
from src.edusign import Edusign
from urllib.parse import urlparse
import datetime
import Yawaei

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

def get_students_ids(edusign_students, intra_students):
    present_students = [a['login'] for a in intra_students 
        if a['status'] == 'present']
    ids = [a['ID'] for a in edusign_students if a['EMAIL'] in present_students]
    return ids

async def sign_single_session(edusign, date, session_index):
    sessions = await get_all_sessions(groups, date)
    if not sessions:
        return None

    # Get Hour of the choosen session
    choices = [min(sessions, key=lambda x: x['end']), max(sessions, key=lambda x: x['begin'])]
    hour = choices[session_index]['begin' if session_index == 0 else 'end'][11:-1]

    # Get session from database
    database_session = get_session_by_date(date, hour)
    if not database_session:
        raise SessionNotCreatedException("Database session not created")

    # Check Approval session state
    if database_session[0]['is_approved'] == 0:
        raise SessionNotValidatedException("Session need validation")

    # Get student attendence list (student_session)
    intra_students = read_student_session(str(database_session[0]['id']))
    # Get Remote students
    remote_students = get_remote_by_date(date)

    # Get Edusign sessions to sign
    to_sign_sessions = [e for e in edusign_sessions if e['begin'][11:-1] == hour or e['end'][11:-1] == hour]

    for to_sign_session in to_sign_sessions:
        try:
            edusign_students = await edusign.get_session_students_to_sign(to_sign_session['edusign_id'])
        except KeyError:
            continue
        ids = get_students_ids(edusign_students, intra_students+remote_students)
        # TODO: return signatures link for professors
        mail = await edusign.send_presence_status(ids, to_sign_session['edusign_id'])
        print(sign, mail)

async def sign_all_sessions(date, session_index):
    """Sign all schools sessions
    """
    edusign = Edusign(options.edusign_secret)
    await sign_single_session(edusign, date, session_index)

def convert_time_utc_local_intra(iso_date):
    date = datetime.datetime.fromisoformat(iso_date)
    return (date + options.timezone.utcoffset(date)).strftime('%H:00')

async def get_all_sessions(groups, session_date):
    edusign = Edusign(options.edusign_secret)
    sessions = []
    for group in groups:
        sessions.append(await edusign.get_sessions(session_date, group))
    return [x for xs in sessions for x in xs]

async def create_single_session(session_date, session_index):
    """Create a session : fetch students, create db session and create students attendance entries
    """
    day = datetime.datetime.strptime(session_date, "%Y-%m-%d").strftime('%A')
    plans = get_weekplan(day)
    groups = [read_promotion(plan['promotion_id'])['sign_id'] for plan in plans]
    sessions = await get_all_sessions(groups, session_date)

    if not sessions:
        raise SessionNotAvailableException(f'No session available for the date {session_date}')

    choices = [min(sessions, key=lambda x: x['end']), max(sessions, key=lambda x: x['begin'])]
    session_hour = choices[session_index]['begin' if session_index == 0 else 'end'][11:-1]

    database_session = get_session_by_date(session_date, session_hour)
    if database_session:
        raise SessionAlreadyCreated(f'Session already created for the date {session_date} and hour {session_hour}')

    session_id = create_session(session_date, session_hour)
    students = []
    for plan in plans:
        students += read_student(plan['promotion_id'])

    for student in students:
        add_student_session(student['login'], student['card'], "NULL", session_id)

async def fetch_session_from_intra(session_id, intra_event):
    Intra = Yawaei.intranet.AutologinIntranet(f'auth-{options.intranet_secret}')
    intra_url = urlparse(intra_event)
    session_path = intra_url.path
    if "registered" in session_path:
        session_path = session_path.replace('/registered', '')
    try:
        students = Intra.get_registered_students(session_path)
    except:
        print(f'Unable to find intranet activity, please provide a correct url : {intra_event} is not valid')
        raise KeyError("Event activity does not exist")

    database_students = read_student_session(session_id)    
    for student in students.keys():
        print(student)
        current_student = list(filter(lambda x: x['login'] == student, database_students))
        if len(current_student) <= 0:
            print(f'Student {student} is present on intra but not in session_student this might be on purpose, skipping...')
            continue
        if current_student[0]['status'] == None or current_student[0]['status'] == 'NULL':
            update_student_session_from_intra(student, students[student], session_id)