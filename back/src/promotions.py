from src.crud.promotion import read_promotion_by_name_date, create_promotion
from src.crud.student import add_student
from src.bocal import card_login, get_user_information
from src.configuration import options
import Yawaei

class BaseCustomException(Exception):
    pass

class PromotionAlreadyCreated(BaseCustomException):
    pass

class PromotionStudentCardMissing(BaseCustomException):
    pass

# TODO: Create student even if there is no card associated
async def create_single_promotion(name, year):
    """Create a promotion entry, create related students from intranet
    """
    database_promotion = read_promotion_by_name_date(name, year)
    if database_promotion == []:
        raise PromotionAlreadyCreated("Promotion already created for {name} and {year}")
    bocal_token = await card_login()
    Intra = Yawaei.intranet.AutologinIntranet(f'auth-{options.intranet_secret}')
    
    students = Intra.get_students(name, year)
    promotion_id = create_promotion(name, year)
    students_card_fail = []
    for student in students:
        try:
            card = await get_user_information(student, bocal_token)
        except KeyError:
            students_card_fail.append(student)
            continue
        add_student(student, card['card_id'], promotion_id)
    
    if len(students_card_fail) > 0:
        raise PromotionStudentCardMissing(f"Please register {' '.join(students_card_fail)} to the bocal access control")
