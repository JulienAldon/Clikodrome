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
        """Log in to edusign using options secrets, will select by default the first school_id
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{options.edusign_url}/professor/account/getByCredentials',
                json={'EMAIL': options.edusign_login, 'PASSWORD': options.edusign_password, 'connexionMode': True}
            ) as resp:
                objs = await resp.json()
                if not objs.get('result'):
                    raise KeyError('No result found')
                objs = objs.get('result')
                school_ids = {}
                if not objs:
                    raise KeyError('No result found')
                print(objs)
                self.token = objs[0]['TOKEN']
                for obj in objs:
                    if not obj.get('TOKEN'):
                        raise KeyError('No token found')
                    if not obj.get('SCHOOL_ID'):
                        raise KeyError('No school id')
                    school_ids.update({_id: obj['TOKEN'] for _id in obj['SCHOOL_ID']})
                self.school_id = school_ids[list(school_ids.keys())[0]]
                return school_ids
        return []
    
    def set_token(self, token):
        """Setter for token
        """
        self.token = token

    def set_school_id(self, school_id):
        """Setter for school_id
        """
        self.school_id = school_id

    async def get_sessions(self, date):
        """Get last edusign sessions given a date
        """
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
        """Return session students for a given session_id
        """
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
        """Return all students_ids for a given session_id
        """
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
                    if not result.get('result'):
                        raise KeyError('No students in session')
                    return result['result']

    async def send_mails(self, student_ids, session_id):
        """Send all emails to students_ids for a given session_id
        """
        remain = await self.get_session_signature(session_id)
        if remain == []:
            return {'result': 'mail already sent'}
        remain_ids = list(filter(lambda x: x in student_ids, remain))
        if remain_ids == []:
            return {'result': 'mail already sent'}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{options.edusign_url}/professor/courses/massSendSignEmail/{self.school_id}/{session_id}',
                json={'studentsId': remain_ids},
                headers={'Authorization': f'Bearer {self.token}'}
            ) as resp:
                return await resp.json()
    
    async def send_lates(self, student_late_ids, session_id):
        """Set delay for all student_late_ids
        """
        res = []
        for late in student_late_ids:
            res.append(await self.send_late(late['ID'], session_id, late['delay']))
        return res

    async def send_late(self, student_id, session_id, late: int):
        """Set delay (late) for a given student in a given session_id
        """
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
        """Sign a single session with signature inside edusign_signature option (base64) given a session_id
        """
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
                remain_ids = []
                for e in a['result']['STUDENTS']:
                    if not e.get('signatureEmail'):
                        remain_ids.append(e['studentId'])
                return remain_ids
        return []