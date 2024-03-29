from datetime import datetime

from apps.app import db
from werkzeug.security import generate_password_hash

class user(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # パスワードを取得しようとすると例外を発生させる
    @property
    def password(self):
        raise AttributeError("読み取り不可")

    # ハッシュ化したパスワードを設定する
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)