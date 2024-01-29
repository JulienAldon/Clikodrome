from src.database import connection
from src.crud.utils import generate_filter_condition

def create_weekplan_entry(day, promotion_id, city):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        INSERT INTO week_plan (day, promotion_id, city)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(t, (day, promotion_id, city))
    except Exception as e:
        print('Error with sql : ', e)
        return False
    connection.commit()
    return cursor.lastrowid

def read_weekplan(id='', day='', city='', promotion_id=''):
    filter_condition, filters = generate_filter_condition(locals())
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from week_plan {filter_condition if filter_condition != 'WHERE' else ''}
    """
    try:
        cursor.execute(t, tuple(filters))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def delete_weekplan(id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        DELETE FROM week_plan WHERE id=%s
    """
    u = f"""
        DELETE FROM session WHERE id=%s
    """
    try:
        cursor.execute(t, (id))
    except Exception as e:
        print('Error with sql :', e)
        return False
    connection.commit()
    return True