from src.database import connection

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

def get_weekplans():
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from week_plan
    """
    try:
        cursor.execute(t)
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def get_weekplan(day, city):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from week_plan WHERE day=%s AND city=%s
    """
    try:
        cursor.execute(t, (day, city))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def get_weekplan_by_promotion(day, city, promo_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from week_plan WHERE day=%s AND city=%s AND promotion_id=%s
    """
    try:
        cursor.execute(t, (day, city, promo_id))
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