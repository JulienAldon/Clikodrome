from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, List
import Yawaei
from pydantic import BaseModel
import datetime
from src.auth import router
from src.identity import token, staff, manager
from src.configuration import options

from src.crud.student import read_student, update_student
from src.crud.student_session import read_student_session, update_student_session
from src.crud.session import read_session, delete_session, update_session
from src.crud.remote import delete_remote, create_remote, read_remote, read_remotes
from src.crud.promotion import delete_promotion, read_promotion
from src.crud.weekplan import delete_weekplan, create_weekplan, read_weekplan
from src.sessions import NoWeekPlanAvailable, get_edusign_sessions_from_database_session, create_database_session, sign_database_session, SessionNotValidatedException, SessionNotAvailableException, SessionAlreadyCreated, fetch_session_from_intra
from src.promotions import create_single_promotion, PromotionAlreadyCreated, SignGroupDoesNotExist
from src.bocal import card_login, get_card_information

from src.edusign import Edusign

app = FastAPI()

origins = [
    options.frontend_uri
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

class RemoteStudent(BaseModel):
    login: str
    begin: str
    end: str

class Student(BaseModel):
    login: str
    session_id: str
    begin: str
    end: str
    id: str

class StudentList(BaseModel):
    data: List[Student]

class StudentElem(BaseModel):
    card: str
    id: str

class SessionCreation(BaseModel):
    sessionIndex: str
    date: str
    city: str

class WeekplanCreation(BaseModel):
    day: str
    promotion_id: str

class PromotionCreation(BaseModel):
    name: str
    sign_id: str
    city: str

class RefreshSession(BaseModel):
    intra_activity_url: str

@app.post('/api/session/{session_id}/refresh', dependencies=[Depends(manager)])
async def refresh_single_session(session_id: str, data: RefreshSession,  token: dict[str, Any] = Depends(token)):
    if not data.intra_activity_url:
        raise HTTPException(status_code=400, detail="Intra activity does not exist")
    try:
        await fetch_session_from_intra(session_id, data.intra_activity_url)
    except KeyError:
        raise HTTPException(status_code=400, detail="Intra activity does not exist")
    return {'result': 'Session refreshed'}

@app.post('/api/session/create', dependencies=[Depends(staff)])
async def add_session(sessionCreation: SessionCreation, token: dict[str, Any] = Depends(token)):
    session_date = sessionCreation.date
    try:
        format_date = datetime.datetime.strptime(session_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        raise HTTPException(status_code=422, detail="Wrong date format")
    if sessionCreation.sessionIndex == '-1' or sessionCreation.sessionIndex == '0':
        try:
            await create_database_session(format_date, int(sessionCreation.sessionIndex), sessionCreation.city)
        except SessionNotAvailableException:
            raise HTTPException(status_code=404, detail="No edusign session available")
        except SessionAlreadyCreated:
            raise HTTPException(status_code=409, detail="Session already created")
        except NoWeekPlanAvailable:
            raise HTTPException(status_code=404, detail="No Weekplan for this day")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400)
    else:
        raise HTTPException(status_code=422)
    return {'result': 'Session created'}

@app.post('/api/session/{session_id}/sign', dependencies=[Depends(manager)])
async def sign_session(session_id: str, token: dict[str, Any] = Depends(token)):
    try:
        res = await sign_database_session(session_id)
    except SessionNotValidatedException:
        raise HTTPException(status_code=400)
    return {'result': res}

@app.post('/api/session/{session_id}', dependencies=[Depends(manager)])
async def validate_session(session_id, token: dict[str, Any] = Depends(token)):
    res = update_session(session_id, 1)
    return {'result': res}    

@app.get('/api/session/{session_id}/signature', dependencies=[Depends(manager)])
async def get_session_professor_signatures(session_id: str, token: dict[str, Any] = Depends(token)):
    edusign = Edusign(options.edusign_secret)
    try:
        sessions = await get_edusign_sessions_from_database_session(session_id)
    except:
        raise HTTPException(status_code=404, detail='Session not found.')
    result = []
    for session in sessions:
        try:
            res = await edusign.get_session_professor_signlink(session['edusign_id'])
            result.append({'login': res['login'], 'link': res['link'], 'state': res['state'], 'session_name': session['name']})
        except Exception:
            continue
    return result

@app.get('/api/sessions/status', dependencies=[Depends(staff)])
async def session_status(token: dict[str, Any] = Depends(token)):
    session_date = datetime.datetime.today()
    format_date = session_date.strftime('%Y-%m-%d')
    sessions = read_session(date=format_date)
    if not sessions:
        return {'result': {
            'morning': None,
            'evening': None,
        }}
    morning = [a for a in sessions if a['hour'] < "12:00:00.000"]
    evening = [a for a in sessions if a['hour'] > "12:00:00.000"]
    return {'result': {
        'morning': morning if morning != [] else None,
        'evening': evening if evening != [] else None
    }}

@app.get('/api/sessions', dependencies=[Depends(staff)])
async def get_sessions(token: dict[str, Any] = Depends(token)):
    sessions = read_session()
    if not sessions:
        HTTPException(status_code=500, detail="Error with the server")
    return {'result': sessions}

@app.get('/api/session/{session_id}', dependencies=[Depends(staff)])
async def get_session(session_id: str, token: dict[str, Any] = Depends(token)):
    try:
        session = read_session(id=session_id)
        students = read_student_session(session_id=session_id)
    except:
        raise HTTPException(status_code=404, detail='Session not found.')
    return {'session': session, 'students': students}

@app.put('/api/session/{session_id}', dependencies=[Depends(staff)])
async def change_session(students: StudentList, session_id: str, token: dict[str, Any] = Depends(token)):
    res = []
    for student in students.data:
        res.append({'login': student.login, 'updated': update_student_session(student.login, student.begin, student.end, session_id)})
    return {'result': res}

@app.put('/api/student/{student_id}', dependencies=[Depends(staff)])
async def change_student(student: StudentElem, student_id, token: dict[str, Any] = Depends(token)):
    res = update_student(student.id, student.card)
    if not res:
        raise HTTPException(status_code=400, detail='Server could not update student')
    return {'result', res}

@app.delete('/api/session/{session_id}', dependencies=[Depends(staff)])
async def remove_session(session_id, token:dict[str, Any] = Depends(token)):
    res = delete_session(session_id)
    if not res:
        raise HTTPException(status_code=400, detail="Server could not delete session")
    return {'result': res}

@app.post('/api/remote', dependencies=[Depends(manager)])
async def add_remote(student: RemoteStudent, token: dict[str, Any] = Depends(token)):
    database_student = read_student(login=student.login)[0]
    already = read_remote(id=database_student['id'])
    res = create_remote(database_student['id'], student.begin, student.end)    
    if not res:
        raise HTTPException(status_code=422)
    return {'result': res}

@app.delete('/api/remote/{remote_id}', dependencies=[Depends(manager)])
async def remove_remote(remote_id: str, token: dict[str, Any] = Depends(token)):
    res = delete_remote(remote_id)
    return {'result': 'Success' if res else 'Error'}

@app.get('/api/remotes', dependencies=[Depends(manager)])
async def get_remotes(token: dict[str, Any] = Depends(token)):
    result = read_remotes()
    return {'result': result}

@app.get('/api/remote/{student_id}', dependencies=[Depends(manager)])
async def get_remotes(student_id: str, token: dict[str, Any] = Depends(token)):
    result = read_remote(student_id=student_id)
    return {'result': result}

@app.get('/api/students', dependencies=[Depends(manager)])
async def get_students(token: dict[str, Any] = Depends(token)):
    database_students = read_student()
    if not database_students:
        raise HTTPException(status_code=404)
    students = [a['login'] for a in database_students]
    result = sorted(list(set(students)))
    return {'result': result}

@app.get('/api/edusign/promotions', dependencies=[Depends(manager)])
async def get_edusign_groups(token: dict[str, Any] = Depends(token)):
    edusign = Edusign(options.edusign_secret)
    try:
        result = await edusign.get_groups()
    except:
        raise HTTPException(status_code=404)
    return result

@app.post('/api/promotion', dependencies=[Depends(manager)])
async def add_promotion(promotion: PromotionCreation, token: dict[str, Any] = Depends(token)):
    try:
        result = await create_single_promotion(promotion.name, promotion.sign_id, promotion.city)
    except PromotionAlreadyCreated:
        raise HTTPException(status_code=409, detail='Promotion already created')
    except SignGroupDoesNotExist:
        raise HTTPException(status_code=404, detail='Cannot find linked edusign promotion')
    return {'result': 'ok'}

@app.get('/api/promotion', dependencies=[Depends(manager)])
async def get_promotion(token: dict[str, Any] = Depends(token)):
    return {'result': read_promotion()}

@app.get('/api/promotion/{promotion_id}', dependencies=[Depends(manager)])
async def get_promotion(promotion_id: str, token: dict[str, Any] = Depends(token)):
    return {'result': {'promotion': read_promotion(id=promotion_id), 'students': read_student(promotion_id=promotion_id)}}

@app.delete('/api/promotion/{promotion_id}', dependencies=[Depends(manager)])
async def remove_promotion(promotion_id: str, token: dict[str, Any] = Depends(token)):
    return {'result': delete_promotion(promotion_id)}

@app.get('/api/weekplan', dependencies=[Depends(manager)])
async def get_weekplan(token: dict[str, Any] = Depends(token)):
    return {'result': read_weekplan()}

@app.post('/api/weekplan', dependencies=[Depends(manager)])
async def add_weekplan(plan: WeekplanCreation, token: dict[str, Any] = Depends(token)):
    promo = read_promotion(id=plan.promotion_id)[0]
    weekplan = read_weekplan(day=plan.day, city=promo['city'], promotion_id=plan.promotion_id)
    print(weekplan)
    if weekplan != ():
        raise HTTPException(status_code=409, detail='Weekplan already created')
    result = create_weekplan(plan.day, plan.promotion_id, promo['city'])
    return {'result': result}

@app.delete('/api/weekplan/{plan_id}', dependencies=[Depends(manager)])
async def remove_weekplan(plan_id: str, token: dict[str, Any] = Depends(token)):
    return {'result': delete_weekplan(plan_id)}