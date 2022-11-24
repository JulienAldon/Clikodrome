from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, List
import Yawaei
from pydantic import BaseModel
import datetime
from src.auth import router
from src.identity import token, staff
from src.configuration import options
from src.crud import read_sessions, read_session, delete_session, delete_remote, read_students, read_all_students, change_student, change_session, create_remote, read_remote, read_remotes
from src.sessions import create_single_session, sign_all_sessions, SessionNotValidatedException, SessionNotAvailableException, SessionAlreadyCreated

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
    status: str
    late: str

class StudentList(BaseModel):
    data: List[Student]

class SessionCreation(BaseModel):
    sessionIndex: str

@app.post('/api/session/create', dependencies=[Depends(staff)])
async def create_session(sessionCreation: SessionCreation, token: dict[str, Any] = Depends(token)):
    session_date = datetime.datetime.today()
    format_date = session_date.strftime('%Y-%m-%d')
    if sessionCreation.sessionIndex == '-1' or sessionCreation.sessionIndex == '0':
        try:
            await create_single_session(format_date, int(sessionCreation.sessionIndex))
        except SessionNotAvailableException:
            raise HTTPException(400, detail="No edusign session available")
        except SessionAlreadyCreated:
            raise HTTPException(400, detail="Session already created")
        except:
            raise HTTPException(400)
    else:
        raise HTTPException(422)
    return {'result': 'Session created'}

@app.post('/api/session/{session_id}/sign', dependencies=[Depends(staff)])
async def sign_session(session_id: str, token: dict[str, Any] = Depends(token)):
    session = read_session(session_id)[0]
    try:
        if session['hour'] < "12:00:00.000":
            await sign_all_sessions(session['date'], 0)
        elif session['hour'] > "12:00:00.000":
            await sign_all_sessions(session['date'], -1)
    except SessionNotValidatedException:
        raise HTTPException(400)
    return {'result': 'ok'}

@app.get('/api/sessions/status', dependencies=[Depends(staff)])
async def session_status(token: dict[str, Any] = Depends(token)):
    session_date = datetime.datetime.today()
    format_date = session_date.strftime('%Y-%m-%d')
    sessions = read_sessions(format_date)
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
    students = read_students(session_id)
    return {'session': session, 'students': students}

@app.put('/api/session/{session_id}', dependencies=[Depends(staff)])
async def modify_session(students: StudentList, session_id: str, token: dict[str, Any] = Depends(token)):
    res = []
    for student in students.data:
        res.append({'login': student.login, 'updated': change_student(student.login, student.status, session_id, student.late)})
    return {'result': res}

@app.delete('/api/session/{session_id}', dependencies=[Depends(staff)])
async def remove_session(session_id, token:dict[str, Any] = Depends(token)):
    res = delete_session(session_id)
    if not res:
        raise HTTPException(400)
    return {'result': res}

@app.post('/api/session/{session_id}', dependencies=[Depends(staff)])
async def validate_session(session_id, token: dict[str, Any] = Depends(token)):
    res = change_session(session_id, 1)
    return {'result': res}    

@app.post('/api/remote', dependencies=[Depends(staff)])
async def add_remote(student: RemoteStudent, token: dict[str, Any] = Depends(token)):
    already = read_remote(student.login)
    res = create_remote(student.login, student.begin, student.end)    
    if not res:
        raise HTTPException(422)
    return {'result': res}

@app.delete('/api/remote/{remote_id}', dependencies=[Depends(staff)])
async def remove_remote(remote_id: str, token: dict[str, Any] = Depends(token)):
    res = delete_remote(remote_id)
    return {'result': 'Success' if res else 'Error'}

@app.get('/api/remotes', dependencies=[Depends(staff)])
async def get_remotes(token: dict[str, Any] = Depends(token)):
    result = read_remotes()
    return {'result': result}

@app.get('/api/remote/{student_id}', dependencies=[Depends(staff)])
async def get_remotes(student_id: str, token: dict[str, Any] = Depends(token)):
    result = read_remote(student_id)
    return {'result': result}

@app.get('/api/students', dependencies=[Depends(staff)])
async def get_students(token: dict[str, Any] = Depends(token)):
    database_students = read_all_students()
    if not database_students:
        raise HTTPException(404)
    students = [a['login'] for a in database_students]
    result = sorted(list(set(students)))
    return {'result': result}