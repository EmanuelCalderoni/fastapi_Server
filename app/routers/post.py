# -*- coding: utf-8 -*-
import datetime

from fastapi import  HTTPException, status , Response, APIRouter, Depends, UploadFile
from .. import squema, oauth2 # mi modelo pydentic para validar request
from ..database import db, bucket
from firebase_admin import firestore


router = APIRouter(
    tags=['Post'])
print("estamos en router. post")

@router.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    # hacemos algo con el archivo recibido...
    myFile = file.file
    myFile.seek(0,2)
    size = myFile.tell()
    myFile.seek(0)
    blob = bucket.blob("myFiles/"+file.filename)
    blob.upload_from_file(myFile)
    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method="GET")
    print (f'\nobjeto almacenado con nombre: {blob.name}\n')
    return {"filename: ": file.filename,
            "content_type: ":file.content_type,
            "size: ":size,
            "URL: ":url}


@router.get("/posts")
async def get_posts(get_current_user:str= Depends(oauth2.get_current_user)):
    posts_ref = db.collection('posts')
    docs = posts_ref.order_by(
        'updated_at',direction=firestore.Query.DESCENDING).stream()
    myData =[]
    for doc in docs:
        post = squema.modelo_respuesta(doc)
        myData.append(post)
    return {"Cantidad":len(myData),
            "data": myData,
            "current_user":get_current_user}


@router.post("/posts")
def create_psot(post: squema.create_Post, get_current_user:str= Depends(oauth2.get_current_user)):
    postByUser = post.dict()
    postByUser ['user'] = get_current_user
    ref_postAgregado =db.collection("posts").document()
    ref_postAgregado.set(postByUser)
    return {"data" : ref_postAgregado.get().to_dict(),
            "ID":ref_postAgregado.id
        }

@router.get("/posts/{id}")
def get_post(id:str):
    ref_post = db.collection('posts').document(id)
    if not ref_post.get().exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post id: {id} was not found')
    return {"data":ref_post.get().to_dict()}

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post (id:str):
    ref_post = db.collection('posts').document(id)
    if not ref_post.get().exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post id: {id} was not found')
    ref_post.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}")
def update_post (id: str, post:squema.update_Post):
    ref_post = db.collection('posts').document(id)
    if not ref_post.get().exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {id} was not found')
    ref_post.update(post.dict())
    return {'message':f'post {id} updated'}