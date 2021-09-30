from flask import session, redirect

def is_login():
    return 'login' in session

def login(user, password):
    if password != '1234':
        return False
    session['login'] = user
    return True

def logout():
    session.pop('login', None)
    return True

def get_user():
    if is_login():
        return session['login']
    return 'not login'
