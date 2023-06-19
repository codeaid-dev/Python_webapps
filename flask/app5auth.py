from flask import session
import os, json, hashlib
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(__file__)
USER_FILE = BASE_DIR + '/data/users.json'
SALT = 'hMLfe:i32n5j#Aiz'

def password_hash(password):
    code = password + SALT
    code = code.encode('utf-8')
    return hashlib.sha256(code).hexdigest()

def password_verify(password, hash):
    verify = password_hash(password)
    return (verify == hash)

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r', encoding='utf-8') as fin:
            return json.load(fin)
    return {}

def save_users(users):
    with open(USER_FILE, 'w', encoding='utf-8') as fout:
        json.dump(users, fout, ensure_ascii=False, indent=2)

def add_user(user, password):
    users = load_users()
    if user in users:
        return False
    #users[user] = password_hash(password)
    users[user] = generate_password_hash(password)
    save_users(users)
    return True

def is_login():
    return 'login' in session

def login(user, password):
    users = load_users()
    if not user in users:
        return False
    if not check_password_hash(users[user], password):
    #if not password_verify(password, users[user]):
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
