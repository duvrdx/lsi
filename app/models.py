from operator import ge
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.filter_by(id=user_id).first()

#Criando classe de usuário/funcionário para login
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def __init__(self, name, username,role, password):
        self.name = name
        self.username = username
        self.role = role
        self.password = generate_password_hash(password)
    
    # Método que checa a senha enviada pelo usuario
    def verify_password(self, pwd_input):
        return check_password_hash(self.password, pwd_input)   

# Classe de Produto
class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcode = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False) # True = Disponível, False = Indisponivel
    
    def __init__(self, name, brand, price, amount, barcode):
        self.name = name
        self.brand = brand
        self.barcode = barcode
        self.price = price
        self.amount = amount
        
        if amount <= 0:
            self.amount = 0
            self.status = False
        else:
            self.status = True

# Classe de Agendamento
class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    provider_name = db.Column(db.String(50), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    
    def __init__(self, provider_name, delivery_date):
        self.provider_name = provider_name
        self.delivery_date = delivery_date