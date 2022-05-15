#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 22:53:34 2022

@author: emanuelcalderoni
"""

from passlib.context import CryptContext
pwd_Context = CryptContext (schemes=["bcrypt"], deprecated = "auto")

def hash(password:str):
    return pwd_Context.hash(password)

def verify(plain_Password, hashed_Password):
    return pwd_Context.verify(plain_Password, hashed_Password,)

