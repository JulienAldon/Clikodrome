from src.database import connection
from src.crud.utils import generate_filter_condition

def read_student_session(id='', session_id='', login='', card='', status='', begin='', end=''):
    filter_condition, filters = generate_filter_condition(locals())
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from student_session {filter_condition if filter_condition != 'WHERE' else ''}
    """
    try:
        cursor.execute(t, tuple(filters))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def update_student_session(login, begin, end, session_id, status='NULL'):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        UPDATE student_session SET begin=%s, end=%s, status=%s WHERE session_id=%s and login=%s
    """
    if begin == 'present':
        begin = 'present'
    else:
        begin = 'NULL'
    if end == 'present':
        end = 'present'
    else:
        end = 'NULL'
    if begin == 'present' and end == 'present':
        status = 'present'
    try:
        cursor.execute(t, (begin, end, status, session_id, login))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True

def create_student_session(login, card, status, begin, end, session_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        INSERT INTO student_session (login, card, status, begin, end, session_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(t, (login, card, status, begin, end, session_id))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return cursor.lastrowid