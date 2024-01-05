from src.configuration import options
from abc import ABC, abstractmethod
import aiohttp

class SignInterface:
    def __init__(self, token, baseurl):
        self.token = token
        self.baseurl = baseurl
    
    async def get_sessions(self, uri, date, group_id):
        """Get last edusign sessions given a date
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{self.baseurl}{uri}?start={date}&end={date}&groupid={group_id}',
                headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
            ) as resp:
                result = await resp.json()
                if not result.get('result'):
                    raise KeyError('No result found')
                return result
        return []

    async def get_session(self, uri, session_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{self.baseurl}{uri}/{session_id}',
                headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
            ) as resp:
                result = await resp.json()
                if not result.get('result'):
                    raise KeyError('No result found')
                return result
        return []

    async def get_groups(self, uri):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{self.baseurl}{uri}',
                headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
            ) as resp:
                result = await resp.json()
                if not result.get('result'):
                    raise KeyError('No result found')
                return result
        return []
    
    async def get_group(self, uri, group_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{self.baseurl}/{uri}/{group_id}',
                headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
            ) as resp:
                result = await resp.json()
                if not result.get('result'):
                    raise KeyError('No result found')
                return result
        return []

    async def get_student(self, uri, student_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{self.baseurl}/{uri}/{student_id}',
                headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
            ) as resp:
                result = await resp.json()
                if not result.get('result'):
                    raise KeyError('No result found')
                return result
        return []

    async def get_session_professor_signlink(self, uri, session_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{self.baseurl}{uri}/{session_id}',
                headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}
            ) as resp:
                result = await resp.json()
                if not result.get('result'):
                    raise KeyError('No result found')
                return result
        return []

    async def send_presence_status(self, uri, student_ids, session_id):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{options.edusign_url}/{uri}/',
                json={'studentsId': student_ids},
                headers={'Authorization': f'Bearer {self.token}'}
            ) as resp:
                return await resp.json()
        return []

class Edusign(SignInterface):
    def __init__(self, token):
        super().__init__(token, "https://ext.edusign.fr/v1")

    async def get_sessions(self, date, group_id):
        result = await super().get_sessions('/course', date, group_id)
        return [{'edusign_id': res['ID'], 'begin': res['START'], 'end': res['END']} for res in result['result']]
    
    async def get_session(self, session_id):
        result = await super().get_session('/course', session_id)
        return result['result']

    async def get_groups(self):
        result = await super().get_groups('/group')
        return [{'ID': a['ID'], 'NAME': a['NAME'], 'STUDENTS': a['STUDENTS']} for a in result['result']]

    async def get_group(self, group_id):
        result = await super().get_group('/group', group_id)
        return {'STUDENTS': result['result']['STUDENTS'], 'ID': result['result']['ID'], 'NAME': result['result']['NAME']}

    async def get_student(self, student_id):
        result = await super().get_student('/student', student_id)
        return {'EMAIL': result['result']['EMAIL'], 'ID': result['result']['ID']}

    async def get_session_professor_signature_status(self, session_id):
        result = await super().get_session('/course', session_id)
        if (result['result']['PROFESSOR_SIGNATURE'] != None \
            and result['result']['PROFESSOR_SIGNATURE'] != '') \
            or (result['result']['PROFESSOR_SIGNATURE_2'] != None \
            and result['result']['PROFESSOR_SIGNATURE_2'] != ''):
            return True
        return False
    
    async def get_session_students_to_sign(self, session_id):
        students_to_sign = []
        result = await super().get_session('/course', session_id)
        for elem in result['result']['STUDENTS']:
            if not elem.get('signatureEmail'):
                students_to_sign.append(elem['studentId'])
        return students_to_sign

    async def get_session_professor_signlink(self, session_id):
        result = await super().get_session_professor_signlink('/course/get-professors-signature-links', session_id)
        return result['result']

    async def send_presence_status(self, student_ids, session_id):
        remain = await self.get_session_students_to_sign(session_id)
        if remain == []:
            return {'result': 'mail already sent'}
        remain_ids = list(filter(lambda x: x in student_ids, remain))
        if remain_ids == []:
            return {'result': 'mail already sent'}
        result = await super().send_presence_status('/course/send-sign-emails', remain_ids, session_id)
        return result