# /auth-service/app/schemas.py
from . import ma
from .models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        # Exclui o hash da senha de qualquer serialização
        exclude = ('password_hash',)