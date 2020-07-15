from flask import Response, request
from flask_restful import Resource
from database.db import db


class Personnels(Resource):
    def get(self):
        personnels = db.collection('users').stream()
        # res = {}
        res = []
        for person in personnels:
            person = person.to_dict()
            # res.update({person.id: person.to_dict()})
            res.append(person)
        return {"results": res}, 200
    
    def post(self):
        body = request.get_json()
        id = body["name"]
        doc_ref = db.collection(u'users').document(id)
        doc_ref.set({
            u'nama_personel': body["name"],
            u'status': body["status"]
        })
        return id, 200

class Personnel(Resource):
    def get(self, id):
        res = []
        person_ref = db.collection(u'users')
        docs = person_ref.where(u'nama_personel', u'==', id).stream()
        for doc in docs:
            res.append(doc.to_dict())
        collections = person_ref.document(id).collections()
        for collection in collections:
            for doc in collection.stream():
                res.append({"kompetensi":doc.to_dict()})
        return {"result": res}, 200

    def put(self, id):
        body = request.get_json()
        if 'status14001' in body:
            print(body)
            person_ref = db.collection(u'users').document(id)
            person_ref.update({
                u'status9001': body['status9001'],
                u'status14001': body['status14001']
            })
        else:
            print("lain")
            person_ref = db.collection(u'users').document(id)
            person_ref.update({
                u'status9001': body['status9001'],
                u'status14001' : None
            })
        return 200

