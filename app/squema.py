#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 21:12:37 2022

@author: emanuelcalderoni
"""

from pydantic import BaseModel,EmailStr
import datetime
from typing import Optional

class Post(BaseModel):
    title :str 
    content: str  
    published: bool = True
    rating: Optional[int] = None
   
    
class create_Post (Post):
    
    created_at = datetime.datetime.now(tz=datetime.timezone.utc)
    updated_at = datetime.datetime.now(tz=datetime.timezone.utc)

    
class update_Post (Post):
    
    updated_at = datetime.datetime.now(tz=datetime.timezone.utc)
    
class User (BaseModel):
    email: EmailStr
    password: str
    created_at = datetime.datetime.now()    

def modelo_respuesta (docSnapshot):
    id = docSnapshot.id
    post=docSnapshot.to_dict()
    response = {
        "ID":id,
        "Title": post["title"],
        "content":post["content"],
        "updated_at":post["updated_at"],
        "user":post["user"]
        }
    return response

def userOut (userSnapshot):
    
    email= userSnapshot.id
    user = userSnapshot.get().to_dict()
    response = {
        "ID":email,
        "created_at":user["created_at"]
        }
    return response

class user_Login (BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str 
    
class Token_data(BaseModel):
    id: Optional [str] = None
    


