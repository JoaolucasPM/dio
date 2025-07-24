from flask import Blueprint, request

from src.app import User, db
from http import HTTPStatus
from flask_jwt_extended import create_access_token


#Criação do blueprint -> nome_blueprint + caminho_arquivo + nome_rota
app = Blueprint("auth", __name__, url_prefix = '/auth')


# Verifica se o usuario está no banco 
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()

    if not user or user.password != password:
        return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {'access_token':access_token}