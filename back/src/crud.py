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
        SELECT * from student_session WHERE session_id=%s
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
        SELECT * from student_session;
    """
    try:
        cursor.execute(t)
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def change_student(login, status, session_id):
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

def update_student(login, status, session_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    if status == 'present':
        status = 'present'
    else:
        status = 'NULL'
    t = f"""
        UPDATE student SET status=%s WHERE session_id=%s and login=%s
    """

    try:
        cursor.execute(t, (status, session_id, login))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True

def get_database_event_by_date(date, hour):
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

def get_database_student(event_id):
    cursor = connection.cursor()
    t = f"""
        SELECT * from student_session WHERE session_id=%s
    """
    try:
        cursor.execute(t, (event_id))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def get_database_session(event_id):
    cursor = connection.cursor()
    t = f"""
        SELECT * from session WHERE id=%s
    """
    try:
        cursor.execute(t, (event_id))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def get_remote_student(date):
    cursor = connection.cursor()
    t = f"""
        SELECT * from remote
    """
    try:
        cursor.execute(t)
        res = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    result = [{**a, 'status': 'present'} for a in res if a['begin'] < date and a['end'] > date]
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

def add_student(login, status, session_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        INSERT INTO student_session (login, status, session_id)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(t, (login, status, session_id))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True

def add_promotion_student(login, card, promotion_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        INSERT INTO student (login, card, promotion_id)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(t, (login, card, promotion_id))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True

def create_promotion(name, year):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        INSERT INTO promotion (name, year)
        VALUES (%s, %s)
    """
    try:
        cursor.execute(t, (name, year))
    except Exception as e:
        print('Error with sql : ', e)
        return False
    connection.commit()
    return cursor.lastrowid

def get_database_promotion_by_name(name, year):
    cursor = connection.cursor()
    t = f"""
        SELECT * from promotion WHERE name=%s and year=%s
    """
    try:
        cursor.execute(t, (name, year))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def create_weekplan_entry(day, promotion_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        INSERT INTO week_plan (day, promotion_id)
        VALUES (%s, %s)
    """
    try:
        cursor.execute(t, (name, year))
    except Exception as e:
        print('Error with sql : ', e)
        return False
    connection.commit()
    return cursor.lastrowid