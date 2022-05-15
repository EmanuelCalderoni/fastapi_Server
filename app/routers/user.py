# -*- coding: utf-8 -*-

from fastapi import HTTPException, status ,  APIRouter
from .. import squema, utils # mi modelo pydentic para validar request
from ..database import db

router = APIRouter(
    tags= ['User'])
print("Estamos en router.user")


@router.post("/user/create",status_code=status.HTTP_201_CREATED)
def create_User(user:squema.User):
    
    hashed_Password=utils.hash(user.password)
    user.password =hashed_Password
    
    ref_User =db.collection("users").document(user.email)
    if ref_User.get().exists:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f'user with email : {user.email} already exists')
    user_paraFirestore = user.dict()
    user_paraFirestore.pop('email')
    ref_User.set(user_paraFirestore)       
    userOut = squema.userOut(ref_User)
    return {"user":userOut}

@router.get("/user/{id}")
def get_user(id:str):
    ref_user = db.collection('users').document(id)
    if not ref_user.get().exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user id: {id} was not found')
    userOut = squema.userOut(ref_user)
    return {"user":userOut} 