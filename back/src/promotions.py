from src.crud.promotion import read_promotion_by_name_date, create_promotion
from src.crud.student import add_student
from src.bocal import card_login, get_user_information
from src.configuration import options
from src.edusign import Edusign

class BaseCustomException(Exception):
    pass

class PromotionAlreadyCreated(BaseCustomException):
    pass

class SignGroupDoesNotExist(BaseCustomException):
    pass

# TODO: Create student even if there is no card associated
async def create_single_promotion(name, sign_id, city):
    """Create a promotion entry, create related students from intranet
    """
    database_promotion = read_promotion_by_name_date(name)
    if database_promotion != ():
        raise PromotionAlreadyCreated("Promotion already created for {name}")
    bocal_token = await card_login()

    edusign = Edusign(options.edusign_secret)
    try:
        group = await edusign.get_group(sign_id)
        students = group['students']
    except KeyError:
        raise SignGroupDoesNotExist(f'The sign group {name} with {sign_id} does not exist.')

    promotion_id = create_promotion(name, sign_id, city)

    for student in students:
        student_info = await edusign.get_student(student)
        student_login = student_info['email']
        try:
            card = await get_user_information(student_login, bocal_token)
        except KeyError:
            card = {'card_id': ''}
        add_student(student_login, card['card_id'], promotion_id)