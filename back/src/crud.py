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

def read_students(session_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from student WHERE session_id=%s
    """
    try:
        cursor.execute(t, (session_id))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def read_all_students():
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from student;
    """
    try:
        cursor.execute(t)
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def change_student(login, status, session_id, late):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        UPDATE student SET status=%s, late=%s WHERE session_id=%s and login=%s
    """
    try:
        cursor.execute(t, (status, late, session_id, login))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True

def delete_session(session_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        DELETE FROM student WHERE session_id=%s
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

def create_remote(login, begin, end):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        INSERT INTO remote (login, begin, end) VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(t, (login, begin, end))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True

def read_remotes():
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from remote
    """
    try:
        cursor.execute(t)
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def read_remote(login):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from remote WHERE login=%s
    """
    try:
        cursor.execute(t, (login))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def delete_remote(_id):
    connection.ping(reconnect=True) 
    cursor = connection.cursor()
    t = f"""
        DELETE FROM remote WHERE id=%s
    """
    try:
        a = cursor.execute(t, (_id))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True
