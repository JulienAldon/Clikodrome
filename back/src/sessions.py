from src.crud.student_session import create_student_session, read_student_session, update_student_session_from_intra
from src.crud.student import read_student
from src.crud.session import read_session, create_session
from src.crud.remote import read_remote_by_date
from src.crud.week_plan import read_weekplan
from src.crud.promotion import read_promotion
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

class NoWeekPlanAvailable(BaseCustomException):
    pass

async def get_students_ids(edusign_students, intra_students):
    edusign = Edusign(options.edusign_secret)
    
    present_students = [a['login'] for a in intra_students 
        if a['status'] == 'present']
    ids = []

    for stud in edusign_students:
        stud_login = await edusign.get_student(stud)
        if stud_login['email'] in present_students:
            ids.append(stud)
    return ids

async def get_edusign_sessions_from_database_session(session_id):
    database_session = read_session(id=session_id)[0]
    if not database_session:
        raise SessionNotCreatedException("Database session not created")

    day = datetime.datetime.strptime(database_session['date'], "%Y-%m-%d").strftime('%A')
    plans = read_weekplan(day=day, city=database_session['city'])
    groups = [read_promotion(id=plan['promotion_id'])[0]['sign_id'] for plan in plans]
    sessions = await get_all_edusign_sessions(groups, database_session['date'])
    if not sessions:
        raise SessionNotAvailableException("No edusign session linked to this clikodrome session")
    to_sign_edusign_sessions = [e for e in sessions if e['begin'][11:-1] == database_session['hour'] or e['end'][11:-1] == database_session['hour']]
    return to_sign_edusign_sessions

async def sign_database_session(session_id):
    database_session = read_session(id=session_id)[0]
    if database_session['is_approved'] == 0:
        raise SessionNotValidatedException("Session need validation")

    sessions = await get_edusign_sessions_from_database_session(session_id)

    remote_students = read_remote_by_date(database_session['date'])
    database_students = read_student_session(session_id=session_id)

    return await sign_edusign_sessions(sessions, database_students+remote_students)

async def sign_edusign_sessions(to_sign_edusign_sessions, students):
    edusign = Edusign(options.edusign_secret)
    result = []
    for to_sign_session in to_sign_edusign_sessions:
        try:
            edusign_students = await edusign.get_session_students_to_sign(to_sign_session['edusign_id'])
        except KeyError:
            continue
        ids = await get_students_ids(edusign_students, students)
        mail = await edusign.send_presence_status(ids, to_sign_session['edusign_id'])
        result.append(mail)
    return result

async def get_all_edusign_sessions(groups, session_date):
    edusign = Edusign(options.edusign_secret)
    sessions = []
    for group in groups:
        try:
            res = await edusign.get_sessions(session_date, group)
            sessions.append(res)
        except KeyError:
            continue
    return [x for xs in sessions for x in xs]

async def create_database_session(session_date, session_index, city):
    """Create a session : fetch students, create db session and create students attendance entries
    """
    day = datetime.datetime.strptime(session_date, "%Y-%m-%d").strftime('%A')
    plans = read_weekplan(day=day, city=city)
    groups = [read_promotion(id=plan['promotion_id'])[0]['sign_id'] for plan in plans]
    if not plans:
        raise NoWeekPlanAvailable(f'No Weekplan for this day {day} and city {city} go to the manager panel to add one.')
    sessions = await get_all_edusign_sessions(groups, session_date)
    if not sessions:
        raise SessionNotAvailableException(f'No session available for the date {session_date}')

    choices = [min(sessions, key=lambda x: x['end']), max(sessions, key=lambda x: x['begin'])]
    session_hour = choices[session_index]['begin' if session_index == 0 else 'end'][11:-1]
    database_session = read_session(date=session_date, hour=session_hour)
    if database_session != ():
        raise SessionAlreadyCreated(f'Session already created for the date {session_date} and hour {session_hour}')

    session_id = create_session(session_date, session_hour, city)
    students = []
    for plan in plans:
        students += read_student(promotion_id=plan['promotion_id'])

    for student in students:
        create_student_session(student['login'], student['card'], "NULL", session_id)

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

    database_students = read_student_session(session_id=session_id)    
    for student in students.keys():
        print(student)
        current_student = list(filter(lambda x: x['login'] == student, database_students))
        if len(current_student) <= 0:
            print(f'Student {student} is present on intra but not in session_student this might be on purpose, skipping...')
            continue
        if current_student[0]['status'] == None or current_student[0]['status'] == 'NULL':
            update_student_session_from_intra(student, students[student], session_id)