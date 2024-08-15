#!/usr/bin/env python3
"""
Main module for any respnse there was a request
"""
import requests

url = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    """Test registeration"""
    endpoint = f'{url}/users'
    data = {'email': email, "password": password}
    response1 = requests.post(endpoint, data=data)
    assert response1.status_code == 200
    assert response1.json() == {"email": email, "message": "user created"}
    respone2 = requests.post(endpoint, data=data)
    assert respone2.status_code == 400
    assert (respone2.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests wrong login"""
    endpoint = f'{url}/sessions'
    data = {'email': email, "password": password}
    response = requests.post(endpoint, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Tests login"""
    endpoint = f'{url}/sessions'
    data = {'email': email, "password": password}
    response = requests.post(endpoint, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """testing data when no user is logged in"""
    endpoint = f'{url}/profile'
    response = requests.get(endpoint)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """testing  when logged in"""
    endpoint = f'{url}/profile'
    cookies = {'session_id': session_id}
    response = requests.get(endpoint, cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id) -> None:
    """Tests log out endpoint"""
    endpoint = f'{url}/sessions'
    cookies = {'session_id': session_id}
    response = requests.delete(endpoint, cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Tests reset password endpoint"""
    endpoint = f'{url}/reset_password'
    response = requests.post(endpoint, data={'email': email})
    assert response.status_code == 200
    assert response.json().get('email') == email
    reset_token = response.json().get('reset_token')
    assert reset_token is not None
    return reset_token


def update_password(email: str, reset_token: str, password: str) -> None:
    """Tests update password endpoint"""
    endpoint = f'{url}/reset_password'
    data = {'email': email, 'reset_token': reset_token, 'password': password}
    response = requests.put(endpoint, data=data)
    assert response.status_code == 200
    assert response.json() == {'email': email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
