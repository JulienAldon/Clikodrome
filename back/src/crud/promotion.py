from src.database import connection

def create_promotion(name, year, sign_name, sign_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        INSERT INTO promotion (name, year, sign_name, sign_id)
        VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(t, (name, year, sign_name, sign_id))
    except Exception as e:
        print('Error with sql : ', e)
        return False
    connection.commit()
    return cursor.lastrowid

def read_promotion_by_name_date(name, year):
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

def read_promotions():
    cursor = connection.cursor()
    t = f"""
        SELECT * from promotion
    """
    try:
        cursor.execute(t)
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def read_promotion(promotion_id):
    cursor = connection.cursor()
    t = f"""
        SELECT * from promotion WHERE id=%s
    """
    try:
        cursor.execute(t, (promotion_id))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def delete_promotion(promotion_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        DELETE FROM week_plan WHERE promotion_id=%s
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