from src.configuration import options
from abc import ABC, abstractmethod
import aiohttp

class Edusign(ABC):
    @abstractmethod
    async def login(self, username, password):
        ...

    @abstractmethod
    async def get_sessions(self, date):
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

    async def login(self, username, password):
        """Log in to edusign using options secrets, will select by default the first school_id
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{options.edusign_url}/professor/account/getByCredentials',
                json={'EMAIL': username, 'PASSWORD': password, 'connexionMode': True}
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
        print(f'signing for {session_id} now')
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
                if (a['result']['PROFESSOR_SIGNATURE'] != None \
                    and a['result']['PROFESSOR_SIGNATURE'] != '') \
                    or (a['result']['PROFESSOR_SIGNATURE_2'] != None \
                    and a['result']['PROFESSOR_SIGNATURE_2'] != ''):
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

# class SignInterface:
#     def __init__(self, token, baseurl):
#         self.token = token
#         self.baseurl = baseurl
    
#     def get_sessions(self, uri, date, group_id):
#         """Get last edusign sessions given a date
#         """
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f'{self.baseurl}{uri}?start={date}&end={date}&groupid={group_id}',
#                 headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
#             ) as resp:
#                 result = await resp.json()
#                 if not result.get('result'):
#                     raise KeyError('No result found')
#                 return result
#         return []

#     def get_session(self, uri, session_id):
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f'{self.baseurl}{uri}/{session_id}',
#                 headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
#             ) as resp:
#                 result = await resp.json()
#                 if not result.get('result'):
#                     raise KeyError('No result found')
#                 return result
#         return []

#     def get_session_professor_signlink(self, uri, session_id):
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f'{self.baseurl}{uri}/{session_id}',
#                 headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
#             ) as resp:
#                 result = await resp.json()
#                 if not result.get('result'):
#                     raise KeyError('No result found')
#                 return result
#         return []

#     def send_presence_status(self, uri, student_ids, session_id):
#         async with aiohttp.ClientSession() as session:
#             async with session.post(
#                 f'{options.edusign_url}/professor/courses/massSendSignEmail/{self.school_id}/{session_id}',
#                 json={'studentsId': remain_ids},
#                 headers={'Authorization': f'Bearer {self.token}'}
#             ) as resp:
#                 return await resp.json()
#         return []

# class Edusign(SignInterface):
#     def __init__(self, token):
#         super().__init__(token, "https://ext.edusign.fr/v1")

#     def get_sessions(self, date, group_id):
#         result = super().get_sessions('/course', date, group_id)
#         return [{'edusign_id': res['ID'], 'begin': res['START'], 'end': res['END']} for res in result['result']]
    
#     def get_session(self, session_id):
#         result = super().get_session('/course', session_id)
#         return result['result']

#     def get_session_professor_signature_status(self, session_id):
#         result = super().get_session('/course', session_id)
#         if (result['result']['PROFESSOR_SIGNATURE'] != None \
#             and result['result']['PROFESSOR_SIGNATURE'] != '') \
#             or (result['result']['PROFESSOR_SIGNATURE_2'] != None \
#             and result['result']['PROFESSOR_SIGNATURE_2'] != ''):
#             return True
#         return False
    
#     def get_session_students_to_sign(self, session_id):
#         students_to_sign = []
#         result = super().get_session('/course', session_id)
#         for elem in result['result']['STUDENTS']:
#             if not elem.get('signatureEmail'):
#                 students_to_sign.append(elem['studentId'])
#         return students_to_sign

#     def get_session_professor_signlink(self, session_id):
#         result = super().get_session_professor_signlink('/course/get-professors-signature-links', session_id)
#         return result['result']

#     def send_presence_status(self, student_ids, session_id):
#         remain = await self.get_session_students_to_sign(session_id)
#         if remain == []:
#             return {'result': 'mail already sent'}
#         remain_ids = list(filter(lambda x: x in student_ids, remain))
#         if remain_ids == []:
#             return {'result': 'mail already sent'}
#         result = super().send_presence_status()
#         return result