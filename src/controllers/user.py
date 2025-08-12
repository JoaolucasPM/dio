from flask import Blueprint, request
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required
from src.ultils import requires_role
from src.views.user import UserSchema,CreatedUserSchema
from src.models.user import User
from src.models.base import  db
from src.app import bcrypt
from marshmallow import ValidationError

#Criação do blueprint -> nome_blueprint + caminho_arquivo + nome_rota
app = Blueprint("user", __name__, url_prefix = '/users')

#Criar o primeiro usuario
@app.route("/init-admin", methods=["POST"])
def init_admin():
     #Verifica se já existe algum usuário no banco
    if db.session.execute(db.select(User)).scalar():
        return {"message": "Usuários já existem, inicialização não permitida"}, HTTPStatus.FORBIDDEN

    data = request.json
    user = User(
        username=data["username"],
        password=bcrypt.generate_password_hash(data["password"]) ,
        role_id=data["role_id"]
    )
    db.session.add(user)
    db.session.commit()
    return {"message": "Admin criado com sucesso!"}, HTTPStatus.CREATED

# Criar usuario
def _create_user():
    user_schema = CreatedUserSchema()
    
    try:
        data = user_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    user = User(
        username = data["username"],
        password=bcrypt.generate_password_hash(data["password"]),
        role_id = data["role_id"]
  
    )
    db.session.add(user)
    db.session.commit()
    return {"Post message":"User created!"}, HTTPStatus.CREATED

# lista usuario ALL
#Protege a rota
@jwt_required()
@requires_role("admin")
def _list_users():
    query = db.select(User)
    users  = db.session.execute(query).scalars()    
    user_schema = UserSchema(many=True)
    return user_schema.dump(users)
    


#http://127.0.0.1:5000/auth/login (GET or POST)
@app.route("/", methods= ['GET', 'POST'])

def handle_user():
   
    if request.method == "POST":
       return _create_user()

        
    else:
        return {'users': _list_users()}
    
    
@app.route('/<int:user_id>') 
def get_user(user_id):
    """User detail view.
    ---
    get:
        parameters:
            - in: path
              name: user_id
              schema: GetUser
        responses:
            200:
                description: Successful operation
                content:
                    application/json:
                        schema: UserSchema
    """    
    user = db.get_or_404(User, user_id)
    return {
        'id': user.id ,
        'username': user.username,
    }


#Update
@app.route('/<int:user_id>', methods=['PATCH']) 
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json    
    mapper = inspect(User)

    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()
    return {
        'id': user.id ,
        'username': user.username
    }

#Delete
@app.route('/<int:user_id>', methods=['DELETE']) 
def delete_user(user_id):
    """User delete view.
    ---
    delete:
        summary: Deletes a pet
        parameters:
            - in: path
              name: user_id
              schema: DeleteUser
        responses:
            204:
                description: Successful operation              
            404:
                description: Invalid pet value              
    """    
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT

