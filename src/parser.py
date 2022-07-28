from src.models.models import Project,Results,Envelope,Material,Construction,Tag
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
from flask import jsonify
import json

db=SQLAlchemy()

class TagTable():
    def insert(self,name,description):
        p=Tag(name,description)

        db.session.add(p)
        db.session.commit()

        return {"status":"success"}

class EnvelopeTable():
    def queryConstruction(self,constructionIds,envelope,key):
        for constructionId in constructionIds:
            construction=Construction.query.filter_by(id=constructionId).first()
            
        envelope[key].append(construction)

        return envelope

    def insert(self,name,description,exWallIds,inWallIds):
        envelope=Envelope(name,description)

        envelopeWithExWall = self.queryConstruction(exWallIds,envelope,"exteriorWall")
        envelopeWithInWall = self.queryConstruction(inWallIds,envelopeWithExWall,"interiorWall")
        envelopeWithRoof = self.queryConstruction(inWallIds,envelopeWithInWall,"roof")

        db.session.add(p)
        db.session.commit()

        return {"status":"success"}
class ConstructionTable():
    def insert(self,name,description,materialIds,thickness,tagIds,categories):
        construction=Construction(
            name,
            description,
            categories,
            thickness
        )
        #extract materials using material_ids
        for materialId in materialIds:
            material=Material.query.filter_by(id=materialId).first()
            construction.materials.append(material)

        for tagId in tagIds:
            tag=Tag.query.filter_by(id=tagId).first()
            construction.tags.append(tag)
        
        #reference: https://stackoverflow.com/questions/24291933/sqlalchemy-object-already-attached-to-session
        current_db_session=db.session.object_session(construction)
        current_db_session.add(construction)
        #db.session.add(construction)
        current_db_session.commit()
        return {"status":"success"}

    def retrieve(self):
        def retrieve_materials(construction):
            materials=[]
            for material in construction.materials:
                temp = {}
                temp['id'] = material.id
                temp['name'] = material.name
                temp['description'] = material.description
                temp['conductivity'] = material.conductivity
                temp['specificHeat'] = material.specificHeat
                temp['density'] = material.density
                materials.append(temp)
            return materials

        def retrieve_tags(construction):
            tags=[]
            for tag in construction.tags:
                temp = {}
                temp['id'] = tag.id
                temp['name'] = tag.name
                tags.append(temp)
            return tags
        
        data = Construction.query.all()
        res = []
        for construction in data:
            temp = {}
            temp['id'] = construction.id
            temp['name'] = construction.name
            temp['description'] = construction.description
            temp['categories'] = construction.categories
            temp['materials'] = retrieve_materials(construction)
            temp['tags'] = retrieve_tags(construction)
            res.append(temp)
        return res

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

    def retrieve(self):
        data=Material.query.all()
        res=[]

        for project in data:
            temp={}
            temp["id"]=project.id
            temp["name"]=project.name
            temp["description"]=project.description
            temp["conductivity"]=project.conductivity
            res.append(temp)

        return res
        

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

    