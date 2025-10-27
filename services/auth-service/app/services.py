# /auth-service/app/services.py
from . import db
from .models import User
from .util.exceptions import UserAlreadyExistsError, AuthenticationError
from flask_jwt_extended import create_access_token
from datetime import timedelta

def register_new_user(form_data):
    email = form_data.get('ds_user_email')
    if User.query.filter_by(ds_user_email=email).first():
        raise UserAlreadyExistsError()

    new_user = User(
        ds_user=form_data.get('ds_user'),
        ds_user_email=email
    )
    new_user.set_password(form_data.get('password'))
    db.session.add(new_user)
    db.session.commit()
    return new_user

def authenticate_user(form_data):
    email = form_data.get('ds_user_email')
    password = form_data.get('password')
    user = User.query.filter_by(ds_user_email=email).first()

    if not user or not user.check_password(password):
        raise AuthenticationError()
    
    expires = timedelta(hours=24)
    access_token = create_access_token(
        identity=str(user.cd_user), 
        expires_delta=expires
    )
    
    return access_token, user