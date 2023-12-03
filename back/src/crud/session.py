from src.database import connection

def read_sessions(date=None):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    if date:
        t = f"""
            SELECT * from session where date=%s
        """
    else:
        t = f"""
            SELECT * from session
        """
    try:
        if date:
            cursor.execute(t, (date))
        else:
            cursor.execute(t)
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def read_session(_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from session WHERE id=%s
    """
    try:
        cursor.execute(t, (_id))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def create_session(date, hour, is_approved=False):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        INSERT INTO session (date, hour, is_approved)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(t, (date, hour, is_approved))
    except Exception as e:
        print('Error with sql : ', e)
        return False
    connection.commit()
    return cursor.lastrowid

def get_session_by_date(date, hour):
    cursor = connection.cursor()
    t = f"""
        SELECT * from session WHERE date=%s and hour=%s
    """
    try:
        cursor.execute(t, (date, hour))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

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

def change_session(session_id, is_approved):
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