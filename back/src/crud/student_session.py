from src.database import connection

def read_student_session(session_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from student_session WHERE session_id=%s
    """
    try:
        cursor.execute(t, (session_id))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def read_student_sessions():
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from student_session;
    """
    try:
        cursor.execute(t)
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def change_student_session(login, status, session_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        UPDATE student_session SET status=%s WHERE session_id=%s and login=%s
    """
    try:
        cursor.execute(t, (status, session_id, login))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True
    
# intra fool proof protection
def update_student_session_from_intra(login, status, session_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    if status == 'present':
        status = 'present'
    else:
        status = 'NULL'
    t = f"""
        UPDATE student_session SET status=%s WHERE session_id=%s and login=%s
    """

    try:
        cursor.execute(t, (status, session_id, login))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True

def add_student_session(login, card, status, session_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        INSERT INTO student_session (login, card, status, session_id)
        VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(t, (login, card, status, session_id))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True