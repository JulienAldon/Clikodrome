from src.database import connection
from src.crud.utils import generate_filter_condition

def create_promotion(name, sign_id, city):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        INSERT INTO promotion (name, sign_id, city)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(t, (name, sign_id, city))
    except Exception as e:
        print('Error with sql : ', e)
        return False
    connection.commit()
    return cursor.lastrowid

def read_promotion(name='', sign_id='', id='', city=''):
    filter_condition, filters = generate_filter_condition(locals())
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from promotion {filter_condition if filter_condition != 'WHERE' else ''}
    """
    try:
        cursor.execute(t, tuple(filters))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def delete_promotion(promotion_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        DELETE FROM weekplan WHERE promotion_id=%s
    """
    w = f"""
        DELETE FROM student WHERE promotion_id=%s
    """
    u = f"""
        DELETE FROM promotion WHERE id=%s
    """
    try:
        cursor.execute(t, (promotion_id))
        cursor.execute(w, (promotion_id))
        cursor.execute(u, (promotion_id))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True