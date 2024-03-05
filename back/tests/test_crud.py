from src.database import connection

from src.crud.utils import generate_filter_condition
from src.crud.promotion import create_promotion, read_promotion, delete_promotion
from src.crud.remote import create_remote, read_remotes, read_remote, read_remote_by_date, delete_remote
from src.crud.student import create_student, read_student
from src.crud.session import create_session, read_session, update_session, delete_session
from src.crud.student_session import read_student_session, update_student_session, create_student_session
from src.crud.weekplan import create_weekplan, read_weekplan, delete_weekplan

from typing import List
import pytest

def clean_db():
    cursor = connection.cursor()
    t = f"DELETE from remote;DELETE from student_session;DELETE from student;DELETE from session;DELETE from weekplan;DELETE from promotion".split(';')
    for a in t:
        cursor.execute(a.strip())

@pytest.fixture
def cleanup():
    yield
    clean_db()

@pytest.fixture
def promotion_init():
    promo1 = create_promotion('Promo1', 'edusign_fake_id', 'LYN')
    promo2 = create_promotion('Promo2', 'edusign_fake_id', 'BDX')
    promo3 = create_promotion('Promo3', 'edusign_fake_id', 'NTS')
    promo4 = create_promotion('Promo4', 'edusign_fake_id', 'PRS')
    student1 = create_student('azer.qsd@epitech.eu', 'fake_card_id', promo1)
    student2 = create_student('jean.jacques@epitech.eu', 'fake_card_id', promo2)
    student3 = create_student('jean.michel@epitech.eu', 'fake_card_id', promo3)
    student4 = create_student('jean.jean@epitech.eu', 'fake_card_id', promo4)
    remote1 = create_remote(student1, '2022-10-10', '2022-12-25')
    remote2 = create_remote(student2, '2023-10-10', '2024-12-25')
    remote3 = create_remote(student3, '2022-10-10', '2022-12-25')
    remote4 = create_remote(student4, '2023-10-10', '2024-12-25')
    weekplan1 = create_weekplan('Monday', promo1, 'LYN')
    weekplan2 = create_weekplan('Thuesday', promo2, 'BDX')
    weekplan3 = create_weekplan('Wednesday', promo3, 'NTS')
    weekplan4 = create_weekplan('Friday', promo4, 'PRS')
    yield [
        promo1, promo2, promo3, promo4, 
        [student1, student2, student3, student4], 
        [remote1, remote2, remote3, remote4], 
        [weekplan1, weekplan2, weekplan3, weekplan4]
    ]

@pytest.fixture
def student_init():
    promo1 = create_promotion('Promo1', 'edusign_fake_id', 'LYN')
    promo2 = create_promotion('Promo2', 'edusign_fake_id', 'BDX')
    student1 = create_student('azer.qsd@epitech.eu', 'fake_card_id', promo1)
    student2 = create_student('jean.jacques@epitech.eu', 'fake_card_id', promo1)
    student3 = create_student('jean.michel@epitech.eu', 'fake_card_id', promo2)
    student4 = create_student('jean.jean@epitech.eu', 'fake_card_id', promo2)
    yield [student1, student2, student3, student4]

@pytest.fixture
def remote_init():
    promo1 = create_promotion('Promo1', 'edusign_fake_id', 'LYN')
    student1 = create_student('azer.qsd@epitech.eu', 'fake_card_id', promo1)
    student2 = create_student('jean.michel@epitech.eu', 'fake_card_id', promo1)
    remote1 = create_remote(student1, '2022-10-10', '2022-12-25')
    remote2 = create_remote(student1, '2023-10-10', '2024-12-25')
    remote3 = create_remote(student2, '2022-10-10', '2022-12-25')
    remote4 = create_remote(student2, '2023-10-10', '2024-12-25')
    yield [remote1, remote2, remote3, remote4, student1, student2]

@pytest.fixture
def session_init():
    session1 = create_session('2024-01-15', '8:30:00', 'LYN')
    session2 = create_session('2024-01-15', '16:30:00', 'LYN')
    session3 = create_session('2024-01-16', '8:30:00', 'BDX')
    session4 = create_session('2024-01-16', '16:30:00', 'BDX')
    yield [session1, session2, session3, session4]

@pytest.fixture
def student_session_init(session_init):
    student_session1 = create_student_session('jean.michel@epitech.eu', 'fake_card_id', 'NULL', session_init[0])
    student_session2 = create_student_session('jean.jacques@epitech.eu', 'fake_card_id', 'NULL', session_init[0])
    student_session3 = create_student_session('jean.pierre@epitech.eu', 'fake_card_id', 'NULL', session_init[0])
    student_session4 = create_student_session('jean.jean@epitech.eu', 'fake_card_id', 'NULL', session_init[0])
    yield [student_session1, student_session2, student_session3, student_session4, session_init[0]]

@pytest.fixture
def weekplan_init(promotion_init):
    weekplan1 = create_weekplan('Monday', promotion_init[0], 'LYN')
    weekplan2 = create_weekplan('Thuesday', promotion_init[1], 'BDX')
    weekplan3 = create_weekplan('Wednesday', promotion_init[2], 'NTS')
    weekplan4 = create_weekplan('Friday', promotion_init[3], 'PRS')
    yield [weekplan1, weekplan2, weekplan3, weekplan4, promotion_init]

def test_generate_filter_condition():
    condition, data = generate_filter_condition({'day': ['Monday'], 'id': 1, 'name': {'aze': 'aze'},
     'city': {}})
    assert condition == 'WHERE day=%s AND id=%s AND name=%s AND city=%s'
    assert data == [['Monday'], 1, {'aze': 'aze'}, {}]
    condition, data = generate_filter_condition({'day': 'Monday', 'id': 1, 'name': 'aze', 'city': 'LYN'})
    assert condition == 'WHERE day=%s AND id=%s AND name=%s AND city=%s'
    assert data == ['Monday', 1, 'aze', 'LYN']
    condition, data = generate_filter_condition({'day': 'Monday'})
    assert condition == 'WHERE day=%s'
    assert data == ['Monday']
    with pytest.raises(Exception) as e_info:
        condition, data = generate_filter_condition(1)
    with pytest.raises(Exception) as e_info:
        condition, data = generate_filter_condition("")
    with pytest.raises(Exception) as e_info:
        condition, data = generate_filter_condition([])

def test_create_promotion(cleanup):
    promo = create_promotion('Promo1', 'edusign_fake_id', 'LYN')
    created_promo = read_promotion(name='Promo1', sign_id='edusign_fake_id', city='LYN', id=promo)
    assert promo != False
    assert created_promo[0] == {'id': promo, 'name': 'Promo1', 'sign_id': 'edusign_fake_id', 'city': 'LYN'}
    
    promo = create_promotion('Promo2', 'edusign_fake_id', 'BDX')
    created_promo = read_promotion(name='Promo2', sign_id='edusign_fake_id', city='BDX', id=promo)
    assert promo != False
    assert created_promo[0] == {'id': promo, 'name': 'Promo2', 'sign_id': 'edusign_fake_id', 'city': 'BDX'}

    with pytest.raises(Exception) as e_info:
        promo = create_promotion()
    promo = create_promotion([], {}, 1)
    assert promo == False
    promo = create_promotion('Promo1', {}, 'BDX')
    assert promo == False
    promo = create_promotion([], 'edusign_fake_id', 'BDX')
    assert promo == False
    promo = create_promotion('Promo1', 'edusign_fake_id', {'a': 'BDX'})
    assert promo == False

def test_read_promotion(cleanup, promotion_init):
    promos = read_promotion()
    assert len(promos) == 4
    assert promos == [
        {'id': promotion_init[0], 'name': 'Promo1', 'sign_id': 'edusign_fake_id', 'city': 'LYN'},
        {'id': promotion_init[1], 'name': 'Promo2', 'sign_id': 'edusign_fake_id', 'city': 'BDX'},
        {'id': promotion_init[2], 'name': 'Promo3', 'sign_id': 'edusign_fake_id', 'city': 'NTS'}, 
        {'id': promotion_init[3], 'name': 'Promo4', 'sign_id': 'edusign_fake_id', 'city': 'PRS'}
    ]
    promos = read_promotion(name='Promo1')
    assert promos[0] == {'id': promotion_init[0], 'name': 'Promo1', 'sign_id': 'edusign_fake_id', 'city': 'LYN'}
    promos = read_promotion(sign_id='edusign_fake_id', city='BDX')
    assert promos[0] == {'id': promotion_init[1], 'name': 'Promo2', 'sign_id': 'edusign_fake_id', 'city': 'BDX'}
    promos = read_promotion(id=promotion_init[2])
    assert promos[0] == {'id': promotion_init[2], 'name': 'Promo3', 'sign_id': 'edusign_fake_id', 'city': 'NTS'}
    promos = read_promotion(id=promotion_init[3], name='Promo4', sign_id='edusign_fake_id', city='PRS')
    assert promos[0] == {'id': promotion_init[3], 'name': 'Promo4', 'sign_id': 'edusign_fake_id', 'city': 'PRS'}

def test_delete_promotion(cleanup, promotion_init):
    promo = delete_promotion(promotion_init[0])
    promos = read_promotion()
    assert promos == [
        {'id': promotion_init[1], 'name': 'Promo2', 'sign_id': 'edusign_fake_id', 'city': 'BDX'},
        {'id': promotion_init[2], 'name': 'Promo3', 'sign_id': 'edusign_fake_id', 'city': 'NTS'}, 
        {'id': promotion_init[3], 'name': 'Promo4', 'sign_id': 'edusign_fake_id', 'city': 'PRS'}
    ]
    assert promo == True
    promo = delete_promotion(0)
    promos = read_promotion()
    assert promo == True
    assert promos == [
        {'id': promotion_init[1], 'name': 'Promo2', 'sign_id': 'edusign_fake_id', 'city': 'BDX'},
        {'id': promotion_init[2], 'name': 'Promo3', 'sign_id': 'edusign_fake_id', 'city': 'NTS'}, 
        {'id': promotion_init[3], 'name': 'Promo4', 'sign_id': 'edusign_fake_id', 'city': 'PRS'}
    ]

def test_create_remote(cleanup, student_init):
    remote = create_remote(student_init[0], '2023-10-24', '2023-11-25')
    remotes = read_remote(begin='2023-10-24', end='2023-11-25', student_id=student_init[0])
    assert remotes[0] == {'id': remote, 'begin': '2023-10-24', 'end': '2023-11-25', 'student_id': student_init[0]}
    assert remote != False

    remote = create_remote(student_init[2], '2023-12-11', '2024-11-25')
    remotes = read_remote(begin='2023-12-11', end='2024-11-25', student_id=student_init[2])
    assert remotes[0] == {'id': remote, 'begin': '2023-12-11', 'end': '2024-11-25', 'student_id': student_init[2]}
    assert remote != False

    with pytest.raises(Exception) as e_info:
        promo = create_remote()
    promo = create_remote([], {}, -1)
    assert promo == False
    promo = create_remote(-1, {}, '2023-10-11')
    assert promo == False
    promo = create_remote([], '2023-10-10', '2023-10-11')
    assert promo == False
    promo = create_remote(-1, '2023-10-10', {'a': '2023-10-10'})
    assert promo == False

def test_read_remotes(cleanup, remote_init):
    remotes = read_remotes()
    assert len(remotes) == 4
    assert remotes == [
        {'begin': '2022-10-10', 'end': '2022-12-25', 'login': 'azer.qsd@epitech.eu', 'id': remote_init[0], 'city': 'LYN'},
        {'begin': '2023-10-10', 'end': '2024-12-25', 'login': 'azer.qsd@epitech.eu', 'id': remote_init[1], 'city': 'LYN'}, 
        {'begin': '2022-10-10', 'end': '2022-12-25', 'login': 'jean.michel@epitech.eu', 'id': remote_init[2], 'city': 'LYN'},
        {'begin': '2023-10-10', 'end': '2024-12-25', 'login': 'jean.michel@epitech.eu', 'id': remote_init[3], 'city': 'LYN'}
    ]

def test_read_remote(cleanup, remote_init):
    remotes = read_remote()
    assert len(remotes) == 4
    assert remotes == [
        {'id': remote_init[0], 'begin': '2022-10-10', 'end': '2022-12-25', 'student_id': remote_init[4]},
        {'id': remote_init[1], 'begin': '2023-10-10', 'end': '2024-12-25', 'student_id': remote_init[4]},
        {'id': remote_init[2], 'begin': '2022-10-10', 'end': '2022-12-25', 'student_id': remote_init[5]},
        {'id': remote_init[3], 'begin': '2023-10-10', 'end': '2024-12-25', 'student_id': remote_init[5]}
    ]
    remotes = read_remote(begin='2022-10-10', end='2022-12-25', student_id=remote_init[4])
    assert remotes[0] == {'id': remote_init[0], 'begin': '2022-10-10', 'end': '2022-12-25', 'student_id': remote_init[4]}
    remotes = read_remote(id=remote_init[1])
    assert remotes[0] == {'id': remote_init[1], 'begin': '2023-10-10', 'end': '2024-12-25', 'student_id': remote_init[4]}
    remotes = read_remote(id=remote_init[2])
    assert remotes[0] == {'id': remote_init[2], 'begin': '2022-10-10', 'end': '2022-12-25', 'student_id': remote_init[5]}
    remotes = read_remote(id=remote_init[3], begin='2023-10-10', end='2024-12-25', student_id=remote_init[5])
    assert remotes[0] == {'id': remote_init[3], 'begin': '2023-10-10', 'end': '2024-12-25', 'student_id': remote_init[5]}

def test_delete_remote(cleanup, remote_init):
    remote = delete_remote(remote_init[0])
    remotes = read_remote()
    assert remotes == [
        {'id': remote_init[1], 'begin': '2023-10-10', 'end': '2024-12-25', 'student_id': remote_init[4]},
        {'id': remote_init[2], 'begin': '2022-10-10', 'end': '2022-12-25', 'student_id': remote_init[5]},
        {'id': remote_init[3], 'begin': '2023-10-10', 'end': '2024-12-25', 'student_id': remote_init[5]}
    ]
    assert remote == True
    remote = delete_remote(0)
    remotes = read_remote()
    assert remote == True
    assert remotes == [
        {'id': remote_init[1], 'begin': '2023-10-10', 'end': '2024-12-25', 'student_id': remote_init[4]},
        {'id': remote_init[2], 'begin': '2022-10-10', 'end': '2022-12-25', 'student_id': remote_init[5]},
        {'id': remote_init[3], 'begin': '2023-10-10', 'end': '2024-12-25', 'student_id': remote_init[5]}
    ]

def test_create_session(cleanup):
    session = create_session('2024-01-15', '8:30:00', 'LYN')
    sessions = read_session(session)
    assert session != False
    assert sessions[0] == {'id': session, 'date': '2024-01-15', 'hour': '8:30:00', 'city': 'LYN', 'is_approved': 0}
    session = create_session('2024-01-16', '16:30:00', 'BDX')
    sessions = read_session(session)
    assert session != False
    assert sessions[0] == {'id': session, 'date': '2024-01-16', 'hour': '16:30:00', 'city': 'BDX', 'is_approved': 0}

    with pytest.raises(Exception) as e_info:
        promo = create_session()
    promo = create_session([], {}, 1)
    assert promo == False
    promo = create_session('date1', {}, 'BDX')
    assert promo == False
    promo = create_session([], 'date2', 'BDX')
    assert promo == False
    promo = create_session('date1', 'date2', {'a': 'BDX'})
    assert promo == False

def test_read_session(cleanup, session_init):
    sessions = read_session()
    assert len(sessions) == 4
    assert sessions == [
        {'id': session_init[0], 'date': '2024-01-15', 'hour': '8:30:00', 'city': 'LYN', 'is_approved': 0},
        {'id': session_init[1], 'date': '2024-01-15', 'hour': '16:30:00', 'city': 'LYN', 'is_approved': 0},
        {'id': session_init[2], 'date': '2024-01-16', 'hour': '8:30:00', 'city': 'BDX', 'is_approved': 0},
        {'id': session_init[3], 'date': '2024-01-16', 'hour': '16:30:00', 'city': 'BDX', 'is_approved': 0}
    ]
    sessions = read_session(date='2024-01-15', hour='8:30:00')
    assert sessions[0] == {'id': session_init[0], 'date': '2024-01-15', 'hour': '8:30:00', 'city': 'LYN', 'is_approved': 0}

    sessions = read_session(id=session_init[1])
    assert sessions[0] == {'id': session_init[1], 'date': '2024-01-15', 'hour': '16:30:00', 'city': 'LYN', 'is_approved': 0}

    sessions = read_session(date='2024-01-16', hour='8:30:00', city='BDX')
    assert sessions[0] == {'id': session_init[2], 'date': '2024-01-16', 'hour': '8:30:00', 'city': 'BDX', 'is_approved': 0}

    sessions = read_session(id=session_init[3], date='2024-01-16', hour='16:30:00', city='BDX')
    assert sessions[0] == {'id': session_init[3], 'date': '2024-01-16', 'hour': '16:30:00', 'city': 'BDX', 'is_approved': 0}

def test_delete_session(cleanup, session_init):
    session = delete_session(session_init[0])
    sessions = read_session()
    assert sessions == [
        {'id': session_init[1], 'date': '2024-01-15', 'hour': '16:30:00', 'city': 'LYN', 'is_approved': 0},
        {'id': session_init[2], 'date': '2024-01-16', 'hour': '8:30:00', 'city': 'BDX', 'is_approved': 0},
        {'id': session_init[3], 'date': '2024-01-16', 'hour': '16:30:00', 'city': 'BDX', 'is_approved': 0}
    ]
    assert session == True
    session = delete_session(0)
    sessions = read_session()
    assert session == True
    assert sessions == [
        {'id': session_init[1], 'date': '2024-01-15', 'hour': '16:30:00', 'city': 'LYN', 'is_approved': 0},
        {'id': session_init[2], 'date': '2024-01-16', 'hour': '8:30:00', 'city': 'BDX', 'is_approved': 0},
        {'id': session_init[3], 'date': '2024-01-16', 'hour': '16:30:00', 'city': 'BDX', 'is_approved': 0}
    ]

def test_update_session(cleanup, session_init):
    session = update_session(session_init[1], 1)
    sessions = read_session(id=session_init[1])
    assert sessions[0] == {'id': session_init[1], 'date': '2024-01-15', 'hour': '16:30:00', 'city': 'LYN', 'is_approved': 1}
    assert session == True

    with pytest.raises(Exception) as e_info:
        session = update_session(0)

def test_create_student_session(cleanup, session_init):
    student_session = create_student_session('jean.jean@epitech.eu', 'fake_card_id', 'NULL', session_init[0])
    student_sessions = read_student_session(login='jean.jean@epitech.eu', session_id=session_init[0])
    assert student_sessions[0] == {'id': student_session, 'login': 'jean.jean@epitech.eu', 'card': 'fake_card_id', 'status': 'NULL', 'session_id': session_init[0]}

    with pytest.raises(Exception) as e_info:
        student_session = create_student_session()

def test_read_student_session(cleanup, student_session_init):
    student_sessions = read_student_session()
    assert len(student_sessions) == 4
    assert student_sessions == [
        {'id': student_session_init[0], 'login': 'jean.michel@epitech.eu', 'card': 'fake_card_id', 'status': 'NULL', 'session_id': student_session_init[4]}, 
        {'id': student_session_init[1], 'login': 'jean.jacques@epitech.eu', 'card': 'fake_card_id', 'status': 'NULL', 'session_id': student_session_init[4]},
        {'id': student_session_init[2], 'login': 'jean.pierre@epitech.eu', 'card': 'fake_card_id', 'status': 'NULL', 'session_id': student_session_init[4]},
        {'id': student_session_init[3], 'login': 'jean.jean@epitech.eu', 'card': 'fake_card_id', 'status': 'NULL', 'session_id': student_session_init[4]}
    ]
    
    student_sessions = read_student_session(login='jean.michel@epitech.eu')
    assert student_sessions[0] == {'id': student_session_init[0], 'login': 'jean.michel@epitech.eu', 'card': 'fake_card_id', 'status': 'NULL', 'session_id': student_session_init[4]}

    student_sessions = read_student_session(id=student_session_init[1])
    assert student_sessions[0] == {'id': student_session_init[1], 'login': 'jean.jacques@epitech.eu', 'card': 'fake_card_id', 'status': 'NULL', 'session_id': student_session_init[4]}

    student_sessions = read_student_session(status='NULL', session_id= student_session_init[4], id=student_session_init[2])
    assert student_sessions[0] == {'id': student_session_init[2], 'login': 'jean.pierre@epitech.eu', 'card': 'fake_card_id', 'status': 'NULL', 'session_id': student_session_init[4]}

    student_sessions = read_student_session(id=student_session_init[3], login='jean.jean@epitech.eu', status='NULL', session_id=student_session_init[4])
    assert student_sessions[0] == {'id': student_session_init[3], 'login': 'jean.jean@epitech.eu', 'card': 'fake_card_id', 'status': 'NULL', 'session_id': student_session_init[4]}

def test_update_student_session(cleanup, student_session_init):
    student_session = update_student_session('jean.jean@epitech.eu', 'present', student_session_init[4])
    student_sessions = read_student_session(login='jean.jean@epitech.eu', session_id=student_session_init[4])
    print(student_sessions)
    assert student_sessions[0] == {'id': student_session_init[3], 'login': 'jean.jean@epitech.eu', 'card': 'fake_card_id', 'status': 'present', 'session_id': student_session_init[4]}
    assert student_session == True

    with pytest.raises(Exception) as e_info:
        session = update_session(0)

def test_create_weekplan(cleanup, promotion_init):
    weekplan = create_weekplan('Monday', promotion_init[0], 'LYN')
    weekplans = read_weekplan(id=weekplan)
    assert weekplan != False
    assert weekplans[0] == {'id': weekplan, 'day': 'Monday', 'city': 'LYN', 'promotion_id': promotion_init[0]}
    weekplan = create_weekplan('Thuesday', promotion_init[1], 'BDX')
    weekplans = read_weekplan(id=weekplan)
    assert weekplan != False
    assert weekplans[0] == {'id': weekplan, 'day': 'Thuesday', 'city': 'BDX', 'promotion_id': promotion_init[1]}

    with pytest.raises(Exception) as e_info:
        weekplan = create_weekplan()    
    weekplan = create_weekplan([], {}, 1)
    assert weekplan == False

def test_read_weekplan(cleanup, weekplan_init):
    weekplans = read_weekplan()
    assert weekplans == [
        {'id': weekplan_init[0], 'day': 'Monday', 'city': 'LYN', 'promotion_id': weekplan_init[4][0]},
        {'id': weekplan_init[1], 'day': 'Thuesday', 'city': 'BDX', 'promotion_id': weekplan_init[4][1]},
        {'id': weekplan_init[2], 'day': 'Wednesday', 'city': 'NTS', 'promotion_id': weekplan_init[4][2]},
        {'id': weekplan_init[3], 'day': 'Friday', 'city': 'PRS', 'promotion_id': weekplan_init[4][3]}
    ]
    weekplans = read_weekplan(id=weekplan_init[0])
    assert weekplans[0] == {'id': weekplan_init[0], 'day': 'Monday', 'city': 'LYN', 'promotion_id': weekplan_init[4][0]}
    weekplans = read_weekplan(id=weekplan_init[1])
    assert weekplans[0] == {'id': weekplan_init[1], 'day': 'Thuesday', 'city': 'BDX', 'promotion_id': weekplan_init[4][1]}
    weekplans = read_weekplan(id=weekplan_init[2], day='Wednesday', city='NTS')
    assert weekplans[0] == {'id': weekplan_init[2], 'day': 'Wednesday', 'city': 'NTS', 'promotion_id': weekplan_init[4][2]}

def test_delete_weekplan(cleanup, weekplan_init):
    weekplan = delete_weekplan(weekplan_init[0])
    weekplans = read_weekplan()
    assert weekplans == [
        {'id': weekplan_init[1], 'day': 'Thuesday', 'city': 'BDX', 'promotion_id': weekplan_init[4][1]},
        {'id': weekplan_init[2], 'day': 'Wednesday', 'city': 'NTS', 'promotion_id': weekplan_init[4][2]},
        {'id': weekplan_init[3], 'day': 'Friday', 'city': 'PRS', 'promotion_id': weekplan_init[4][3]}
    ]
    assert weekplan == True
    weekplan = delete_weekplan(0)
    weekplans = read_weekplan()
    assert weekplan == True
    assert weekplans == [
        {'id': weekplan_init[1], 'day': 'Thuesday', 'city': 'BDX', 'promotion_id': weekplan_init[4][1]},
        {'id': weekplan_init[2], 'day': 'Wednesday', 'city': 'NTS', 'promotion_id': weekplan_init[4][2]},
        {'id': weekplan_init[3], 'day': 'Friday', 'city': 'PRS', 'promotion_id': weekplan_init[4][3]}
    ]
