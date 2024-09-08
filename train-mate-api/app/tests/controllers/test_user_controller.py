import pytest
from unittest.mock import patch
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client



@patch('app.controllers.user_controller.verify_token_service')
@patch('app.controllers.user_controller.save_user_info_service')
def test_save_user_info_should_return_created(mock_save_user_info, mock_verify_token_service, client):
    mock_verify_token_service.return_value = 'fake_uid'


    response = client.post('/save_user_info', json={
        'full_name': 'John Doe',
        'gender': 'Male',
        'weight': '70',
        'height': '180'
    }, headers={'Authorization': 'Bearer fake_token'})

    assert response.status_code == 201

    mock_save_user_info.assert_called_once_with('fake_uid', {
        'full_name': 'John Doe',
        'gender': 'Male',
        'weight': '70',
        'height': '180'
    })

@patch('app.controllers.user_controller.verify_token_service')
@patch('app.controllers.user_controller.save_user_info_service')
def test_save_user_info_with_invalid_token_should_return_401(mock_save_user_info, mock_verify_token_service, client):
    mock_verify_token_service.return_value = None


    response = client.post('/save_user_info', json={
        'full_name': 'John Doe',
        'gender': 'Male',
        'weight': '70',
        'height': '180'
    }, headers={'Authorization': 'Bearer fake_token'})

    assert response.status_code == 401
    mock_save_user_info.assert_not_called()