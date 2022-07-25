from src.models.models import Project,Results,Material,Construction
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
from flask import jsonify
import json

db=SQLAlchemy()

class ConstructionTable():
    def 

class MaterialTable():
    def insert(self,name,description,conductibity,specificHeat,density,moistureConductivity,moistureCapacity):
        p=Material(
            name,
            description,
            conductibity,
            specificHeat,
            density,
            moistureConductivity,
            moistureCapacity
        )
        db.session.add(p)
        db.session.commit()

        return p
        

class ProjectTable():
    def delete(self,id):
        sql1 = delete(Project.__table__).where(Project.id==id)
        db.session.execute(sql1)
        db.session.commit()
        return {"status":"success"}

    def insert(self,name):
        p=Project(name=name)
        db.session.add(p)
        db.session.commit()

        return p
    
    def retrieve(self):
        data=Project.query.all()
        res=[]

        for project in data:
            temp={}
            temp["id"]=project.id
            temp["name"]=project.name
            #temp["results"]=project.results
            res.append(temp)

        return res

class ResultTable():
    def delete(self,project_id):
        sql1 = delete(Results.__table__).where(Results.project_id==project_id)
        db.session.execute(sql1)
        db.session.commit()
        return {"status":"success"}

    def insert(self,hour,roomT,clodS,rhexS,ahexS,fs,roomH,clodL,rhexL,ahexL,fl,mrt):
        p=Results(hour=hour,roomT=roomT,clodS=clodS,rhexS=rhexS,ahexS=ahexS,fs=fs,roomH=roomH,clodL=clodL,rhexL=rhexL,ahexL=ahexL,fl=fl,mrt=mrt)
        db.session.add(p)
        db.session.commit()

        return p

    def retrieve(self, project_id):
        #data=Result.query.filter(Result.project_id.any(project_id=project_id))
        data=Results.query.filter_by(project_id=project_id)
        #data=Result.query.all()
        res=[]
        roomId=1
        for room in data:
            print ('room',room)
            result={}
            result["roomT"]=list(json.loads(room.roomT).values())
            result["clodS"]=list(json.loads(room.clodS).values())
            result["rhexS"]=list(json.loads(room.rhexS).values())
            result["ahexS"]=list(json.loads(room.ahexS).values())
            result["fs"]=list(json.loads(room.fs).values())
            result["roomH"]=list(json.loads(room.roomH).values())
            result["clodL"]=list(json.loads(room.clodL).values())
            result["rhexL"]=list(json.loads(room.rhexL).values())
            result["ahexL"]=list(json.loads(room.ahexL).values())
            result["fl"]=list(json.loads(room.fl).values())
            result["mrt"]=list(json.loads(room.mrt).values())
            result["hour"]=list(room.hour.values())
            results={"roomId":roomId,"results":result}
            res.append(results)
            roomId+=1

        #print ('res')
        return res

    