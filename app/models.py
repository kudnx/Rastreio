from operator import index
from app import db

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64), index=True)
    cod = db.Column(db.String(13))

    def __repr__(self):
        return '<Encomenda {}>'.format(self.description)

class PackageInformation():
    quantity = 0
    cod      = ""
    descricao_envio = ""
    destinatario = ""

    def __repr__(self):
        return '<Informação da Encomenda {}>'.format(self.quantity)