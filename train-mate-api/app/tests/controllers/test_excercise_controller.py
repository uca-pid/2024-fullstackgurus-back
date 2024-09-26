import pytest
from unittest.mock import patch
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

@patch('app.controllers.excercise_controller.save_exercise')
def test_save_exercise_should_return_created(mock_save_exercise, client):

    response = client.post('/api/exercise/save-exercise', json={
        'name': 'salto en largo',
        'calories_per_hour': 5000,
        'public': "False"
    })

    assert response.status_code == 201
    assert response.json == {
        'message': 'Exercise saved successfully',
        'data': {
            'name': 'salto en largo',
            'calories_per_hour': 5000,
            'public': "False"
        }
    }


def test_save_exercise_missing_calories_per_hour_should_return_400(client):
    response = client.post('/api/exercise/save-exercise', json={
        'name': 'salto en largo',
        'public': True
    })

    assert response.status_code == 400
    assert response.json == {"error": "Missing data"}



def test_save_exercise_missing_public_should_return_400(client):
    response = client.post('/api/exercise/save-exercise', json={
        'name': 'salto en largo',
        'calories_per_hour': 5000,
    })

    assert response.status_code == 400
    assert response.json == {"error": "Missing data"}

def test_save_exercise_missing_name_should_return_400(client):
    response = client.post('/api/exercise/save-exercise', json={
        'calories_per_hour': 5000,
        'public': True
    })

    assert response.status_code == 400
    assert response.json == {"error": "Missing data"}