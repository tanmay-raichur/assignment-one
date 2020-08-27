import requests
#from first_flask import return_json, upload_file
#from unittest.mock import patch

def test_welcome_page():
    response = requests.get("http://127.0.0.1:5000/")
    assert response.status_code == 200


def test_json_page():
    response = requests.get("http://127.0.0.1:5000/converted-json")
    assert response.status_code in (200, 400)


def test_post_request():
    response = requests.post("http://127.0.0.1:5000/upload-file")
    assert response.status_code in (200, 400)


#@patch('first_flask.requests.post')
#def test_post_request(mock_get):
#    mock_get.return_value.status_code = 200
#    response = upload_file()
#    assert response.status_code == 200


