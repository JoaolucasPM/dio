from src.app import ma
from marshmallow import fields
from src.models.user import User
from src.views.role import RoleSchema

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
    

class GetUser(ma.Schema):
    user_id = fields.Int(required=True, strict=True)  

class DeleteUser(ma.Schema):
    user_id = fields.Int(required=True, strict=True)  

    
class CreatedUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True, strict=True)
    
    class Meta:
        fields = ("username", "password", "role_id")