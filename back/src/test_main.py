from fastapi.testclient import TestClient
from src.main import app
from src.crud.session import read_session
from src.crud.week_plan import read_weekplan
from src.crud.promotion import read_promotion
import pytest
from typing import List
from src.identity import token, manager, staff

client = TestClient(app)

async def override_dependency():
    return {'intra-role': 'pedago'}

def test_create_promotion():
    response = client.post('/api/promotion', json={
        'year': '2023',
        'name': 'LYN202',
        'sign_id': 'g2yjmdyh6hbnvfk',
        'city': 'LYN'
    })
    assert response.status_code == 200
    assert response.json() == {'result': 'ok'}
    new_promo = read_promotion(id=1)
    assert new_promo == {
        'id': 1,
        'name': 'LYN202',
        'sign_id': 'g2yjmdyh6hbnvfk',
        'year': '2023',
        'city': 'LYN'
    }

def test_read_promotion():
    response = client.get('/api/promotion')
    assert response.status_code == 200
    assert response.json() == {'result': read_promotion()}

def test_create_weekplan():
    response = client.post('/api/weekplan', json={
        'day': 'Friday',
        'promotion_id': 1
    })
    assert response.status_code == 200
    assert response.json() == {'result': 1}
    weekplan = read_weekplan(day='Friday', city='LYN')
    assert weekplan == [{'id': 1, 'day': 'Friday', 'city': 'LYN', 'promotion_id': 1}]

def test_read_weekplan():
    response = client.get('/api/weekplan')
    assert response.status_code == 200
    assert response.json() == {'result': read_weekplan()}

def test_session_create():
    response = client.post('/api/session/create', json={
        'sessionIndex': 0, 
        'date': '2024-01-18', 
        'city': 'LYN'
    })
    session = read_session(date='2024-01-18')

    assert response.status_code == 200
    print(response.json())
    assert response.json() == {'result': 'Session created'}
    assert session.date == '2024-01-18'
    assert session.hour <= '12:00:00'
    assert session.city == 'LYN'

def test_read_sessions():
    response = client.get('/api/sessions')

    assert response.status_code == 200
    assert response.json() == {'result': read_session()}

def test_read_session():
    response = client.get('/api/session/1')
    assert response.status_code == 200
    assert response.json() == {read_session(id=1)}

def test_validate_session():
    session = client.post('/api/session/1')
    tmp_session = read_session(id=1)

    assert session.status_code == 200
    assert session.json() == {'result': True}
    assert tmp_session['is_approved'] == '1'

def test_delete_session():
    tmp_session = read_session()
    session = client.delete('/api/session/1')
    assert session.status_code == 200
    assert session.json() == {'result': True}
    assert len(read_session()) == len(tmp_session) - 1

def test_delete_weekplan():
    tmp_len = len(read_weekplan())
    response = client.delete('/api/weekplan/1')
    weekplans = read_weekplan()
    assert response.status_code == 200
    assert response.json() == {'result': True}
    assert len(weekplans) == tmp_len - 1

def test_delete_promotion():
    tmp_len = len(read_promotion())
    response = client.delete('/api/promotion/1')
    assert response.status_code == 200
    assert response.json() == {'result': True}
    promotions = read_promotion()
    assert len(promotions) == tmp_len - 1

app.dependency_overrides[token] = override_dependency

# TODO: change src.crud.weekplans to match other patterns