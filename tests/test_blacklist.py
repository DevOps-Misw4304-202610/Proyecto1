import json
from unittest.mock import patch, MagicMock
from app.models import Blacklist

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    #assert response.status_code == 500 #prueba para provocar error 
    assert response.json['status'] == "UP"

@patch('app.resources.db.session')
def test_add_to_blacklist_success(mock_session, client, auth_header):
    # Simulamos que el guardado en base de datos es exitoso
    payload = {
        "email": "test@uniandes.edu.co",
        "app_uuid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "blocked_reason": "Spam bot"
    }
    
    response = client.post('/blacklists', 
                           data=json.dumps(payload), 
                           headers={**auth_header, "Content-Type": "application/json"})
    
    assert response.status_code == 201
    assert mock_session.add.called
    assert mock_session.commit.called

def test_add_to_blacklist_invalid_email(client, auth_header):
    # La validación de Marshmallow ocurre antes de tocar la DB
    payload = {"email": "not-an-email", "app_uuid": "123"}
    response = client.post('/blacklists',
                           data=json.dumps(payload),
                           headers={**auth_header, "Content-Type": "application/json"})
    
    assert response.status_code == 400
    # Cambiamos esta línea para acceder a la llave 'errors'
    assert "email" in response.json["errors"]

@patch('app.models.Blacklist.query')
def test_check_email_exists(mock_query, client, auth_header):
    # Simulamos que la consulta devuelve un registro existente
    mock_blacklist_entry = MagicMock(spec=Blacklist)
    mock_blacklist_entry.email = "exist@test.com"
    mock_blacklist_entry.blocked_reason = "Reason"
    
    mock_query.filter_by.return_value.first.return_value = mock_blacklist_entry
    
    response = client.get('/blacklists/exist@test.com', headers=auth_header)
    
    assert response.status_code == 200
    assert response.json['present'] is True

@patch('app.models.Blacklist.query')
def test_check_email_not_exists(mock_query, client, auth_header):
    # Simulamos que la consulta no encuentra nada
    mock_query.filter_by.return_value.first.return_value = None
    
    response = client.get('/blacklists/noexiste@test.com', headers=auth_header)
    
    assert response.status_code == 200
    assert response.json['present'] is False

def test_unauthorized_access(client):
    # Verifica que el decorador @jwt_required() funcione
    response = client.get('/blacklists/any@test.com')
    assert response.status_code == 401