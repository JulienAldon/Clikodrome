from src.crud import update_student, get_database_event_by_date, get_database_student, get_database_session, get_remote_student, create_session, add_student, add_promotion_student, create_promotion, get_database_promotion_by_name, create_weekplan_entry
from src.bocal import card_login, get_user_information
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

def get_any_student_name(entry: dict[str, Any]) -> str | None:
    return entry.get('EMAIL', entry.get('login', None))

def get_students_ids(edusign_students, intra_students):
    present_students = [a['login'] for a in intra_students 
        if a['status'] == 'present']
    ids = [a['ID'] for a in edusign_students if a['EMAIL'] in present_students]
    return ids

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

class PromotionAlreadyCreated(BaseCustomException):
    pass

class PromotionStudentCardMissing(BaseCustomException):
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
        ids = get_students_ids(edusign_students, intra_students+remote_students)
        sign = await edusign.sign_session(to_sign_session['edusign_id'])
        mail = await edusign.send_mails(ids, to_sign_session['edusign_id'])
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

def convert_time_utc_local_intra(iso_date):
    date = datetime.datetime.fromisoformat(iso_date)
    return (date + options.timezone.utcoffset(date)).strftime('%H:00')

async def get_edusign_sessions(edusign, school_ids, session_date):
    sessions = []
    for school_id, token in list(school_ids.items()):
        edusign.set_school_id(school_id)
        edusign.set_token(token)
        school_session = await edusign.get_sessions(session_date)
        sessions += school_session
    return sessions

async def create_single_session(session_date, session_index):
    """Create a session : fetch students, create db session and create students attendance entries
    """

    edusign = EdusignToken()
    for cred in options.all_edusign_credentials:
        school_ids = await edusign.login(cred['login'], cred['password'])
        sessions = await get_edusign_sessions(edusign, school_ids, session_date)
        if not sessions:
            if cred == options.all_edusign_credentials[-1]:
                raise SessionNotAvailableException(f'No session available for the date {session_date}')
            continue

        choices = [min(sessions, key=lambda x: x['end']), max(sessions, key=lambda x: x['begin'])]
        session_hour = choices[session_index]['begin' if session_index == 0 else 'end'][11:-1]

        database_session = get_database_event_by_date(session_date, session_hour)
        if database_session:
            raise SessionAlreadyCreated(f'Session already created for the date {session_date} and hour {session_hour}')

        session_id = create_session(session_date, session_hour)
        session_hour = convert_time_utc_local_intra(f'{session_date} {session_hour}')
        # Intra = Yawaei.intranet.AutologinIntranet(f'auth-{options.intranet_secret}')

        # intra_session = Intra.get_events(
        #     options.event_activity,
        #     date=session_date,
        #     hour=session_hour
        # )
        # students = Intra.get_registered_students(options.event_activity + intra_session[0])
        # Get students from promotion registered today (Monday, Tuesday, Wednesday, Thursday, Friday)
        for student in students.keys():
            add_student(student, students[student], session_id)
        if session_id:
            return

async def create_single_promotion(name, year):
    """Create a promotion entry, create related students from intranet
    """
    database_promotion = get_database_promotion_by_name(name, year)
    if database_promotion == []:
        raise PromotionAlreadyCreated("Promotion already created for {name} and {year}")
    bocal_token = await card_login()
    Intra = Yawaei.intranet.AutologinIntranet(f'auth-{options.intranet_secret}')
    
    students = Intra.get_students(name, year)
    promotion_id = create_promotion(name, year)
    students_card_fail = []
    for student in students:
        try:
            card = await get_user_information(student, bocal_token)['card_id']
        except KeyError:
            students_card_fail.append(student)
        add_promotion_student(student, card, promotion_id)
    
    if len(students_card_fail) > 0:
        raise PromotionStudentCardMissing(f"Please register {' '.join(students_card_fail)} to the bocal access control")

async def create_weekplan(plan):
    """
    plan format : {'Monday': [promotion_id], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
    """
    for day in plan.keys():
        for promo in plan[day]:
            create_weekplan_entry(day, promo)
    return 'Created'

# FIXME
async def refresh_session(session_id):
    pass
    # Intra = Yawaei.intranet.AutologinIntranet(f'auth-{options.intranet_secret}')
    # res = get_database_session(session_id)
    # if len(res) != 1:
    #     raise KeyError('Session not found')
    # session_date = res[0]['date']
    # session_hour = res[0]['hour']
    # session_hour = convert_time_utc_local_intra(f'{session_date} {session_hour}')

    # intra_session = Intra.get_events(
    #     options.event_activity,
    #     date=session_date,
    #     hour=session_hour
    # )

    # students = Intra.get_registered_students(options.event_activity + intra_session[0])

    # database_students = get_database_student(session_id)    
    # for student in students.keys():
    #     current_student = list(filter(lambda x: x['login'] == student, database_students))
    #     if current_student[0]['status'] == None or current_student[0]['status'] == 'NULL':
    #         update_student(student, students[student], session_id)