from flask import Blueprint, request
from http import HTTPStatus
from flask_jwt_extended import create_access_token

from src.models.user import User
from src.models.base import db
from src.app import bcrypt

#Criação do blueprint -> nome_blueprint + caminho_arquivo + nome_rota
app = Blueprint("auth", __name__, url_prefix = '/auth')

def _check_password(password_has, password_raw):
    return bcrypt.check_password_hash(password_has, password_raw)   
    
# Verifica se o usuario está no banco 
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()

    if not user or not _check_password(user.password, password):
        return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {'access_token':access_token}