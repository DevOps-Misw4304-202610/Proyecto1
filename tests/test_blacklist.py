import json

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == "UP"

def test_add_to_blacklist_success(client, auth_header):
    payload = {
        "email": "test@uniandes.edu.co",
        "app_uuid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "blocked_reason": "Spam bot"
    }
    response = client.post('/blacklists', 
                           data=json.dumps(payload), 
                           headers={**auth_header, "Content-Type": "application/json"})
    assert response.status_code == 201
    assert "id" in response.json

def test_add_to_blacklist_invalid_email(client, auth_header):
    payload = {"email": "not-an-email", "app_uuid": "123"}
    response = client.post('/blacklists', 
                           data=json.dumps(payload), 
                           headers={**auth_header, "Content-Type": "application/json"})
    assert response.status_code == 400
    assert "email" in response.json

def test_check_email_exists(client, auth_header):
    # Primero insertamos
    client.post('/blacklists', 
                data=json.dumps({"email": "exist@test.com", "app_uuid": "123"}), 
                headers={**auth_header, "Content-Type": "application/json"})
    
    # Luego consultamos
    response = client.get('/blacklists/exist@test.com', headers=auth_header)
    assert response.status_code == 200
    assert response.json['present'] is True

def test_unauthorized_access(client):
    response = client.get('/blacklists/any@test.com')
    assert response.status_code == 401