from src.database import connection
from src.crud.utils import generate_filter_condition

def create_student(login, card, promotion_id):
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

def read_student(id='', login='', card='', promotion_id=''): 
    filter_condition, filters = generate_filter_condition(locals())
    connection.ping(reconnect=True)
    cursor = connection.cursor()
    t = f"""
        SELECT * from student {filter_condition if filter_condition != 'WHERE' else ''}
    """
    try:
        cursor.execute(t, tuple(filters))
        result = cursor.fetchall()
    except Exception as e:
        print('Error with sql :', e)
        return False
    return result