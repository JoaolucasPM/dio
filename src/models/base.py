
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

# SQLAlchemy ->  Conexao com o banco 
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
"""  """
migrate = Migrate()

#JWT
jwt = JWTManager()
