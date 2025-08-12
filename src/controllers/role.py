from flask import Blueprint, request
from http import HTTPStatus

from src.models.roles import Role
from src.models.base import db

#Criação do blueprint -> nome_blueprint + caminho_arquivo + nome_rota
app = Blueprint("role", __name__, url_prefix = '/roles')

@app.route("/", methods= ['POST'])
def create_role():
    data = request.json
    role = Role(name=data['name'])
    db.session.add(role)
    db.session.commit()
    
    return {"message": "Role created"}, HTTPStatus.CREATED
