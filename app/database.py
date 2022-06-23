
import time
import firebase_admin
from firebase_admin import credentials, firestore,storage


def conectarFirestore():
    while True:
        try:
            cred = credentials.Certificate('fastapi-nonsql-f0e5d77d929b.json')
            firebase_admin.initialize_app(cred,{'storageBucket': 'fastapi-nonsql.appspot.com'})
            db = firestore.client()
            bucket = storage.bucket()
            print('\n\nDatabase connected succesfully  !\n\n')
            return (db,bucket)
        except Exception as error:
            print('Database failed connection : ',error)
            time.sleep(2)
          
print ("va a comenzar la conexion a  Firestore...")
db, bucket = conectarFirestore()

