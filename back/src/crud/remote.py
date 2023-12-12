from src.database import connection

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

def get_remote_by_date(date):
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
