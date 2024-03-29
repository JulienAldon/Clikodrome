from src.database import connection
from src.crud.utils import generate_filter_condition

def read_session(id='', date='', hour='', is_approved='', city=''):
    filter_condition, filters = generate_filter_condition(locals())
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from session {filter_condition if filter_condition != 'WHERE' else ''}
    """
    try:
        cursor.execute(t, tuple(filters))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def create_session(date, hour, city, is_approved=False):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        INSERT INTO session (date, hour, is_approved, city)
        VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(t, (date, hour, is_approved, city))
    except Exception as e:
        print('Error with sql : ', e)
        return False
    connection.commit()
    return cursor.lastrowid

def delete_session(session_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        DELETE FROM student_session WHERE session_id=%s
    """
    u = f"""
        DELETE FROM session WHERE id=%s
    """
    try:
        cursor.execute(t, (session_id))
        cursor.execute(u, (session_id))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True

def update_session(session_id, is_approved):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        UPDATE session SET is_approved=%s WHERE id=%s
    """
    try:
        cursor.execute(t, (is_approved, session_id))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True