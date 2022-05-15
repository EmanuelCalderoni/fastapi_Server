# -*- coding: utf-8 -*-

from datetime import datetime,timedelta
from jose import jwt,JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from . import squema
from .config import settings

oauth2_squeme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() +timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encode_jwt

def verify_token(token:str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY)
        id:str =payload.get('user_id')
        if id is None:
            raise credential_exception
        token_data =squema.Token_data(id=id)
    except JWTError:
        raise credential_exception
    
    return token_data

def get_current_user (token:str=Depends(oauth2_squeme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='could ++not validate credentials',
                                         headers={'WWW-Authenticate':'Bearer'}
                                         )
    token_data = verify_token(token, credential_exception) 
    current_user= token_data.id                                                              
    return current_user