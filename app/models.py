from operator import index
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64), index=True)
    cod = db.Column(db.String(13))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def package_description(cod):
        return Package.query.filter_by(cod=cod).first()

    def __repr__(self):
        return '<Encomenda {}>'.format(self.description)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    package = db.relationship('Package', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def user_packages(self):
        return Package.query.filter_by(user_id=self.id).order_by(Package.id.desc())

    def __repr__(self):
        return '<Usuário {}>'.format(self.username)

class PackageInformation():
    quantity = 0
    cod      = ""
    categoty = ""
    recipient = ""
    data = [[]]
    

    def __repr__(self):
        return '<Informação da Encomenda {}>'.format(self.quantity)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))