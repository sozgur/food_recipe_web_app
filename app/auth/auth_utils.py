import os
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.models import db


# create token for user 
def token_generator(user):
    s = Serializer(os.environ.get('SECRET_KEY'), expires_in=3600)
    token = s.dumps({'id': user.id})

    return token


# get user_id from token
def token_get_user_id(token):
    s = Serializer(os.environ.get('SECRET_KEY'))
    try:
        data = s.loads(token)
    except:
        return False

    return data.get('id')
    
