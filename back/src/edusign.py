from src.configuration import options
from abc import ABC, abstractmethod
import aiohttp
from src.configuration import options

class Edusign(ABC):
    @abstractmethod
    async def login(self):
        ...

    @abstractmethod
    async def get_sessions(self, date):
        ...
    
    async def get_session(self, session_id):
        ...

    @abstractmethod
    async def get_students(self, session_id):
        ...

    @abstractmethod
    async def send_mails(self, student_ids, session_id):
        ...

    @abstractmethod
    async def sign_session(self, session_id):
        ...
    
    @abstractmethod
    async def get_session_professor_signature(self, session_id):
        ...
    
    @abstractmethod
    async def get_session_signature(self, session_id):
        ...

class EdusignToken(Edusign):
    def __init__(self):
        self.token = ''
        self.school_id = ''

    async def login(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{options.edusign_url}/professor/account/getByCredentials',
                json={'EMAIL': options.edusign_login, 'PASSWORD': options.edusign_password}
            ) as resp:
                obj = await resp.json()
                if not obj.get('result'):
                    raise KeyError('No result found')
                if not obj['result'].get('TOKEN'):
                    raise KeyError('No token found')
                self.token = obj['result']['TOKEN']
                if not obj['result'].get('SCHOOL_ID'):
                    raise KeyError('No school id')
                self.school_id = obj['result']['SCHOOL_ID'][0]
                return True

    async def get_sessions(self, date):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{options.edusign_url}/professor/courses/getCourses/getLastProfessorCourses/{self.school_id}?start={date}&end={date}',
                headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
            ) as resp:
                result = await resp.json()
                if not result.get('result'):
                    raise KeyError('No result found')
                return [{'edusign_id': res['COURSE_ID'], 'begin': res['START'], 'end': res['END']} for res in result['result']['result']]

    async def get_session(self, session_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{options.edusign_url}/professor/courses/{self.school_id}/{session_id}',
                headers={'Authorization': f'Bearer {self.token}'}
            ) as resp:
                result = await resp.json()
                if not result.get('result') and result.get('status') != 'success':
                    print(result)
                    raise KeyError('No result found')
                return result['result']['STUDENTS']

    async def get_students(self, session_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{options.edusign_url}/professor/courses/{self.school_id}/{session_id}',
                headers={'Authorization': f'Bearer {self.token}'}
            ) as resp:
                result = await resp.json()
                if not result.get('result'):
                    raise KeyError('No result found')
                student_ids = [c['studentId'] for c in result['result']['STUDENTS']]
                async with session.post(
                    f'{options.edusign_url}/professor/students/getManyAttendanceList/{self.school_id}/',
                    json={'studentIds': student_ids},
                    headers={'Authorization': f'Bearer {self.token}'}
                ) as response:
                    result = await response.json()
                    return result['result']

    async def send_mails(self, student_ids, session_id):
        if await self.get_session_signature(session_id):
            return {'result': 'mail already sent'}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{options.edusign_url}/professor/courses/massSendSignEmail/{self.school_id}/{session_id}',
                json={'studentsId': student_ids},
                headers={'Authorization': f'Bearer {self.token}'}
            ) as resp:
                return await resp.json()
    
    async def send_lates(self, student_late_ids, session_id):
        res = []
        for late in student_late_ids:
            res.append(await send_lates(late['ID'], session_id, late['delay'])
        return res

    async def send_late(self, student_id, session_id, late: int):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{options.edusign_url}/professor/courses/student-delay/{self.school_id}/{session_id}',
                json={
                    'delay': late,
                    'studentId': student_id
                },
                headers={'Authorization': f'Bearer {self.token}'}
            ) as resp:
                return await resp.json()
        

    async def sign_session(self, session_id):
        if await self.get_session_professor_signature(session_id):
            return {"result": "session already signed"}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{options.edusign_url}/professor/courses/setProfessorSignature/{self.school_id}/{session_id}',
                json={'base64Signature': options.edusign_signature},
                headers={'Authorization': f'Bearer {self.token}'}
            ) as resp:
                return await resp.json()
    
    async def get_session_professor_signature(self, session_id):
        """Check professor signature present for a given session
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{options.edusign_url}/professor/courses/{self.school_id}/{session_id}',
                headers={'Authorization': f'Bearer {self.token}'}
            ) as resp:
                a = await resp.json()
                if a['result']['PROFESSOR_SIGNATURE'] != None or a['result']['PROFESSOR_SIGNATURE_2'] != None:
                    return True
        return False
    
    async def get_session_signature(self, session_id):
        """Check if a session has any email already sent
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{options.edusign_url}/professor/courses/{self.school_id}/{session_id}',
                headers={'Authorization': f'Bearer {self.token}'}
            ) as resp:
                a = await resp.json()
                for e in a['result']['STUDENTS']:
                    if e['state']:
                        return True
        return False