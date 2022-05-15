#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 19:54:10 2022

@author: emanuelcalderoni 
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from random import randrange
#import firebase_admin
#from firebase_admin import credentials, firestore
#from . import squema, utils # mi modelo pydentic para validar request
from .routers import post,user,auth


print("estamos en main!")  

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hola Mundo !"}




       
"""

                Temas vistos al 3/4/2022:
                    * uvicorn main:app --reload
                    * postman: guardar request
                    * metodo, path y function an argument (post:Post    basemodel, pydantic)
                    * get post put y delete
                    * crud con listas para almacenar
                    * json -> dict -> almacenamiento
                    * lista -> JSON automatico realizado por @app
                    
                Temas visto al 9/4:
                    * httpExeption si no encuentra el id
                    *status: 200,201,204,404
                    *response(status_code)
                    *for i,p in enumerate( my_Posts)  i es indice y p es post:Post
                    *post:BaseModel , si viene del front-end un body lo asigna a post
                    
                notas 10/4:
                    * este archivo main ejecuta su codigo cuando inicia el uvicorn,
                       aqui se debe conectar a la base de datos.
                       
                notas 16/04: NSQL database 
                    * pasar datos de fastapi a firestore
                    * primero agregar un valor de time stamp en el dict: 
                        "created_at":datetime.datetime.now(tz=datetime.timezone.utc)
                    * crear una referencia a un docuemnto nuevo con un ID automatico: 
                        ref_postAgregado =db.collection("posts").document()
                    * Agregar dato:
                        ref_postAgregado.set(post_paraFirestore)
                    * Obtener datos:
                        return {"data" : ref_postAgregado.get().to_dict(),
                            "ID":ref_postAgregado.id}
                    * not Found 404:
                        ref_post = db.collection('posts').document(id):  id es type str
                        if not ref_post.get().exists:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                detail=f'post id: {id} was not found')
                    * update:
                        obtener una referencia al doc
                        luego modificar los campos (update no borra los campos que no se modifican):
                            city_ref.update({u'capital': True, "updated_at":firestore.SERVER_TIMESTAMP})
                    * query:
                        posts_ref = db.collection('posts')
                        docs = posts_ref.order_by(
                            'title',direction=firestore.Query.DESCENDING).stream()
                notas 17/04:
                    * post:Post se convierte a dictionary con .dict() y ya esta listo para firestore
                    * the squema/ pandentic model define the structure of a request & response
                    * Conclusion: nuestro pandentic model difiere de nuestro documento Firestore en el indice automatico y los time
                    stamp
                    * from . import squema # mi modelo pydentic para validar request esta en otro file
                    *arme una funcion que personaliza el modelo de respuesta de la api dentro del modulo squema

                notas 19/04:
                    * cree una collecion user
                    * email es parte del modelo pandentic
                    * en mi collecion email es la id porque es unica
                    * eliminar la key 'email' de user:  myDict.pop('email')
                    
                notas 21/09 :
                    *ref_doc.id : id del doc (su nombre)
                    *ref_doc.get().to_dict(): datos del doc
                    *creamos un userOut para excluir de nuestra respuesta json el campo password 
                    
                notas 23/4:
                    * email_vcalidator
                    * hash password: se paso toda la logica a el archivo utils
                
                notas 25/4:
                    * refactorizamos con router y database
                    *pasamos variables entre modulos:  db es la ref a firestore y pasa a routers
                    
                notas 1/5:AUTHENTICATION
                
                    * El usuario debe ser creado, se recibe del /post usuario:email y password:str
                    * el password se encripta en el modulo utils
                    * se crea el documento id:email con el campo : hashed_password
                    
                    * El usuario debe logearse, se reciben las credenciales definidas como OAuth2PasswordRequestForm
                    * se obtiene del documento la hashed_password y se verifican las credenciales
                    * se crea el token, con el email del usuario se codifica el token en el modulo oauth2
                    * el token combina una secret_key, algorithm , time expire y nuestro email que viene del formulario
                    
                    * El usuario autenticado puede utilizar la api, se recibe un GET con Headers 'Authorization':Bearer + el token
                    * Se llama a la funcion get_current_user del modulo oauth2 , la que busca el token con OAuth2PasswordBearer
                    * Se decodifica el token que contiene nuestro user_id que es el usuario autenticado
                    * Si falla la validacion de la token ya sea porque no esta autenticado 
                      o expira la sesion se informa status.HTTP_401_UNAUTHORIZED.
                      
                    * el current_user se utiliza para setear el campo user de los post en la base de datos
                      y para acceder a los recursos de la API segun sus permisos.
                    * Aclaracion: el current_user en mi caso es el email el cual es un string, si quisiera obtener 
                      sus datos debo obtenerlos de la base de datos como lo hicieron en el tutorial.
                    
                Notas 7/05:Postman Environments
                    * se creo en DEV y PROD la variable URL
                    * seteamos la variable  JWT con el token de nuestra API
                      
                Notas 14/05: ENV variables
                    * seteamos una variable en el terminal: export SECRETKEY="myKey"
                    * importamos su valor a python : import os; key = os.getev("SECRETKEY")
                    * seteamos SECRETKEY,ALGORITHM, ACCESS_EXPIRE en config.py, el cual accede a .env
                    * .env debe estar afuera de la carpeta app para que la lea pydantic
                    * editamos el archivo .gitignore
                        
"""


