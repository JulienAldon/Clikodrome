from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, List
import Yawaei
from pydantic import BaseModel
import datetime
from src.auth import router
from src.identity import token, staff, manager
from src.configuration import options

from src.crud.student_session import read_student_session, read_student_sessions, change_student_session
from src.crud.session import read_sessions, read_session, delete_session, change_session
from src.crud.remote import delete_remote, create_remote, read_remote, read_remotes
from src.crud.promotion import read_promotions, delete_promotion, read_promotion
from src.crud.week_plan import get_weekplans, delete_weekplan, create_weekplan_entry
from src.sessions import create_single_session, sign_single_session, SessionNotValidatedException, SessionNotAvailableException, SessionAlreadyCreated, fetch_session_from_intra
from src.promotions import create_single_promotion, PromotionStudentCardMissing
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
    status: str
    id: str

class StudentList(BaseModel):
    data: List[Student]

class SessionCreation(BaseModel):
    sessionIndex: str
    date: str
    city: str

class WeekplanCreation(BaseModel):
    day: str
    promotion_id: str

class PromotionCreation(BaseModel):
    year: str
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
async def create_session(sessionCreation: SessionCreation, token: dict[str, Any] = Depends(token)):
    session_date = sessionCreation.date
    try:
        format_date = datetime.datetime.strptime(session_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    except:
        raise HTTPException(status_code=422, detail="Wrong date format")
    if sessionCreation.sessionIndex == '-1' or sessionCreation.sessionIndex == '0':
        try:
            await create_single_session(format_date, int(sessionCreation.sessionIndex), sessionCreation.city)
        except SessionNotAvailableException:
            raise HTTPException(status_code=400, detail="No edusign session available")
        except SessionAlreadyCreated:
            raise HTTPException(status_code=400, detail="Session already created")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400)
    else:
        raise HTTPException(status_code=422)
    return {'result': 'Session created'}

@app.post('/api/session/{session_id}/sign', dependencies=[Depends(manager)])
async def sign_session(session_id: str, token: dict[str, Any] = Depends(token)):
    try:
        await sign_single_session(session_id)
    except SessionNotValidatedException:
        raise HTTPException(status_code=400)
    return {'result': 'ok'}

@app.get('/api/sessions/status', dependencies=[Depends(staff)])
async def session_status(token: dict[str, Any] = Depends(token)):
    session_date = datetime.datetime.today()
    format_date = session_date.strftime('%Y-%m-%d')
    sessions = read_sessions(format_date)
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
    sessions = read_sessions()
    return {'result': sessions}

@app.get('/api/session/{session_id}', dependencies=[Depends(staff)])
async def get_session(session_id: str, token: dict[str, Any] = Depends(token)):
    session = read_session(session_id)
    students = read_student_session(session_id)
    return {'session': session, 'students': students}

@app.put('/api/session/{session_id}', dependencies=[Depends(staff)])
async def modify_session(students: StudentList, session_id: str, token: dict[str, Any] = Depends(token)):
    res = []
    for student in students.data:
        res.append({'login': student.login, 'updated': change_student_session(student.login, student.status, session_id)})
    return {'result': res}

@app.delete('/api/session/{session_id}', dependencies=[Depends(staff)])
async def remove_session(session_id, token:dict[str, Any] = Depends(token)):
    res = delete_session(session_id)
    if not res:
        raise HTTPException(status_code=400)
    return {'result': res}

@app.post('/api/session/{session_id}', dependencies=[Depends(manager)])
async def validate_session(session_id, token: dict[str, Any] = Depends(token)):
    res = change_session(session_id, 1)
    return {'result': res}    

@app.post('/api/remote', dependencies=[Depends(manager)])
async def add_remote(student: RemoteStudent, token: dict[str, Any] = Depends(token)):
    already = read_remote(student.login)
    res = create_remote(student.login, student.begin, student.end)    
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
    result = read_remote(student_id)
    return {'result': result}

@app.get('/api/students', dependencies=[Depends(manager)])
async def get_students(token: dict[str, Any] = Depends(token)):
    database_students = read_student_sessions()
    if not database_students:
        raise HTTPException(status_code=404)
    students = [a['login'] for a in database_students]
    result = sorted(list(set(students)))
    return {'result': result}
 
# @app.get('/api/scan/card/{card_id}', dependencies=[Depends(staff)])
# async def read_card(card_id: str, token: dict[str, Any] = Depends(token)):
#     bocal_token = await card_login()
#     try:
#         result = await get_card_information(card_id, bocal_token)
#     except KeyError:
#         raise HTTPException(404)
#     return result

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
        result = await create_single_promotion(promotion.name, promotion.year, promotion.sign_id, promotion.city)
    except PromotionStudentCardMissing as e:
        return {'result': e}
    return {'result': 'ok'}

@app.get('/api/promotion', dependencies=[Depends(manager)])
async def get_promotion(token: dict[str, Any] = Depends(token)):
    return {'result': read_promotions()}

@app.delete('/api/promotion/{promotion_id}', dependencies=[Depends(manager)])
async def remove_promotion(promotion_id: str, token: dict[str, Any] = Depends(token)):
    return {'result': delete_promotion(promotion_id)}

@app.get('/api/weekplan', dependencies=[Depends(manager)])
async def read_weekplan(token: dict[str, Any] = Depends(token)):
    return {'result': get_weekplans()}

@app.post('/api/weekplan', dependencies=[Depends(manager)])
async def add_weekplan(plan: WeekplanCreation, token: dict[str, Any] = Depends(token)):
    promo = read_promotion(plan.promotion_id)
    result = create_weekplan_entry(plan.day, plan.promotion_id, promo['city'])
    return {'result': result}

@app.delete('/api/weekplan/{plan_id}', dependencies=[Depends(manager)])
async def remove_weekplan(plan_id: str, token: dict[str, Any] = Depends(token)):
    return {'result': delete_weekplan(plan_id)}

# @app.put('/api/weekplan/{plan_id}', dependencies=[Depends(manager)])
# async def read_promotion(plan: WeekplanCreation, plan_id: str, token: dict[str, Any] = Depends(token)):
#     return {'result': read_promotions()}