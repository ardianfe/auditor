from flask import Response, request
from database.db import db
from flask_restful import Resource
from docx2python import docx2python
from datetime import datetime


class UploadFile(Resource):
    def post(self):
        # print(request.files)
        if 'file' not in request.files:
            return "No file found"
        f = request.files['file']
        doc_result = docx2python(f)

        iso9001_status = ''
        iso14000_status = ''
        tanggal_evaluasi = doc_result.body[0][0][1][0].partition('\t: ')[2]
        name = doc_result.body[0][0][0][0].partition('\t: ')[2]
        status = doc_result.body[0][1][1][0].partition('\t: ')[2]
        
        
        #  this is code for check oputput of template
        '''
        check_name = doc_result.body[0][0][0][0]
        print(check_name) 
        '''

        data = {}
        sektor = {}
        for i in range(1,14):
            sektor.update({doc_result.body[8][i][0][0]:int(doc_result.body[8][i][5][0])})

        keys_9001 = ['12', '14', '16', '17', '18', '19', '22', '28', '29', '33', '34', '35', '36']
        keys_14000 = ['12', '14', '16', '17', '18', '19', '22', '28', '34']

        sektor_9001 = {x:sektor[x] for x in keys_9001}
        sektor_14000 = {x:sektor[x] for x in keys_14000}
        

        data["kompetensi"] = {}
        data["kompetensi"]["iso9001"] = {}
        data["kompetensi"]["iso14000"] = {}
        data["kompetensi"]["iso9001"]["calon_auditor"] = {}
        data["kompetensi"]["iso9001"]["auditor"] = {}
        data["kompetensi"]["iso9001"]["lead_auditor"] = {}
        data["kompetensi"]["iso14000"]["calon_auditor"] = {}
        data["kompetensi"]["iso14000"]["auditor"] = {}
        data["kompetensi"]["iso14000"]["lead_auditor"] = {}
        data["kompetensi"]["iso9001"]["sektor"] = {}
        data["kompetensi"]["iso14000"]["sektor"] = {}


        data["kompetensi"]["iso9001"]["calon_auditor"]["status"] = int(doc_result.body[10][2][5][0])
        data["kompetensi"]["iso9001"]["calon_auditor"]["tanggal_valid"] = tanggal_evaluasi

        data["kompetensi"]["iso9001"]["auditor"]["status"] = int(doc_result.body[10][3][5][0])
        if data["kompetensi"]["iso9001"]["auditor"]["status"] == 1:
            data["kompetensi"]["iso9001"]["auditor"]["tanggal_valid"] = tanggal_evaluasi

        data["kompetensi"]["iso9001"]["lead_auditor"]["status"] = int(doc_result.body[10][4][5][0])
        if data["kompetensi"]["iso9001"]["lead_auditor"]["status"] == 1:
            data["kompetensi"]["iso9001"]["lead_auditor"]["tanggal_valid"] = tanggal_evaluasi

        data["kompetensi"]["iso14000"]["calon_auditor"]["status"] = int(doc_result.body[10][6][5][0])
        data["kompetensi"]["iso14000"]["calon_auditor"]["tanggal_valid"] = tanggal_evaluasi

        data["kompetensi"]["iso14000"]["auditor"]["status"] = int(doc_result.body[10][7][5][0])
        if data["kompetensi"]["iso14000"]["auditor"]["status"] == 1:
            data["kompetensi"]["iso14000"]["auditor"]["tanggal_valid"] = tanggal_evaluasi

        data["kompetensi"]["iso14000"]["lead_auditor"]["status"] = int(doc_result.body[10][8][5][0])
        if data["kompetensi"]["iso14000"]["lead_auditor"]["status"] == 1:
            data["kompetensi"]["iso14000"]["lead_auditor"]["tanggal_valid"] = tanggal_evaluasi

        data["kompetensi"]["iso9001"]["sektor"] = sektor_9001
        data["kompetensi"]["iso14000"]["sektor"] = sektor_14000

        if data["kompetensi"]["iso14000"]["lead_auditor"]["status"] == 1:
            iso14000_status = "LA"
        elif data["kompetensi"]["iso14000"]["auditor"]["status"] == 1:
            iso14000_status = "A"
        else:
            iso14000_status = "LA"

        if data["kompetensi"]["iso9001"]["lead_auditor"]["status"] == 1:
            iso9001_status = "LA"
        elif data["kompetensi"]["iso9001"]["auditor"]["status"] == 1:
            iso9001_status = "A"
        else:
            iso9001_status = "LA"
        
        print(iso14000_status)
        print(iso9001_status)

        doc_ref = db.collection(u'users').document(name)
        doc_ref.set({
            u'nama_personel': name,
            u'status': status,
            u'iso9001_status': iso9001_status,
            u'iso14000_status': iso14000_status
        })

        kompt_ref = doc_ref.collection(u'kompetensi').document()
        kompt_ref.set({
            u'iso9001': data["kompetensi"]["iso9001"],
            u'iso14000': data["kompetensi"]["iso14000"]
        })
        return {'nama_personel': name}, 200

