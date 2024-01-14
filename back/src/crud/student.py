from src.database import connection

def add_student(login, card, promotion_id):
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

def read_student_from_promotion(promotion_id):
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from student WHERE promotion_id=%s
    """
    try:
        cursor.execute(t, (promotion_id))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def read_student(login): 
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from student WHERE login=%s
    """
    try:
        cursor.execute(t, (login))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result

def read_students(): 
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from student
    """
    try:
        cursor.execute(t)
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result