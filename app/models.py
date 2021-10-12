from operator import index
from app import db

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64), index=True)
    cod = db.Column(db.String(13))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Encomenda {}>'.format(self.description)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    package = db.relationship('Package', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<Usuário {}>'.format(self.username)

class PackageInformation():
    quantity = 0
    cod      = ""
    categoria = ""
    destinatario = ""
    dados = [[]]

    def __repr__(self):
        return '<Informação da Encomenda {}>'.format(self.quantity)