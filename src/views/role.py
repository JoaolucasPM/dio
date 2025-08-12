from marshmallow import Schema, fields
from src.app import ma 


class RoleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    

    class Meta:
        fields = ("id", "name")
    