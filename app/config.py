# -*- coding: utf-8 -*-

import os
from pydantic import BaseSettings

valueKey = os.getenv("valueKEY")
print(valueKey)

class Settings (BaseSettings):
    SECRET_KEY :str
    ALGORITHM :str
    ACCESS_TOKEN_EXPIRE_MINUTES :int
    
    class Config:
        env_file = ".env"

settings = Settings()


