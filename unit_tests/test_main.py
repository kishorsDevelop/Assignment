from main import app
import jwt

fake_token = jwt.encode(
            {"user_id": 1},
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )
headers = {'Authorization': 'Bearer ' + fake_token}

def test_get_notes():
    response = app.test_client().get('/api/notes', headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json, list) 

def test_post_notes():
    response = app.test_client().post('/api/notes', headers=headers, data={'content': 'fake_data', 'title': 'test'})
    assert response.status_code == 201

def test_get_notes_by_id():
    fake_id = 1
    response = app.test_client().get(f'/api/notes/{fake_id}', headers=headers)
    assert response.status_code == 200

def test_delete_notes_by_id():
    fake_id = 1
    response = app.test_client().delete(f'/api/notes/{fake_id}', headers=headers)
    assert response.status_code == 200

def test_put_notes_by_id():
    fake_id = 1
    response = app.test_client().put(f'/api/notes/{fake_id}', headers=headers, data={'content': 'test'})
    assert response.status_code == 200

def test_share_notes():
    fake_id = 1
    response = app.test_client().post(f'/api/notes/{fake_id}/share', headers=headers)
    assert response.status_code == 200

    
