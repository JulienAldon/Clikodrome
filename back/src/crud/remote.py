from src.database import connection
from src.crud.utils import generate_filter_condition

def create_remote(student_id, begin, end):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        INSERT INTO remote (student_id, begin, end) VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(t, (student_id, begin, end))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return cursor.lastrowid

def read_remotes():
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT remote.begin, remote.end, student.login, remote.id, promotion.city from remote JOIN student ON student.id=remote.student_id JOIN promotion ON student.promotion_id = promotion.id;
    """
    try:
        cursor.execute(t)
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def read_remote_by_date(date):
    connection.ping(reconnect=True)
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

def read_remote(id='', begin='', end='', student_id=''):
    filter_condition, filters = generate_filter_condition(locals())
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from remote {filter_condition if filter_condition != 'WHERE' else ''}
    """
    try:
        cursor.execute(t, tuple(filters))
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
