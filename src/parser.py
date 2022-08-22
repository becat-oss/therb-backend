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

        return p

    def retrieve(self):
        p=Tag.query.all()
        tags=[]
        for tag in p:
            temp = {}
            temp['id'] = str(tag.id)
            temp['name'] = tag.name
            tags.append(temp)
        return tags

class EnvelopeTable():
    def queryConstruction(self,constructionId,envelope,key):
        # for constructionId in constructionIds:
        #     construction=Construction.query.filter_by(id=constructionId).first()
        construction=Construction.query.filter_by(id=constructionId).first()
            
        envelope[key].append(construction)

        return envelope

    def insert(self,name,description,exWallId,inWallId,roofId,groundFloorId,floorCeilingId,windowId):
        envelope=Envelope(name,description)

        # envelopeWithExWall = self.queryConstruction(exWallId,envelope,"exteriorWall")
        # envelopeWithInWall = self.queryConstruction(inWallId,envelopeWithExWall,"interiorWall")
        # envelopeWithRoof = self.queryConstruction(roofId,envelopeWithInWall,"roof")
        # envelopeWithGroundFloor = self.queryConstruction(groundFloorId,envelopeWithRoof,"groundFloor")
        # envelopeWithFloorCeiling = self.queryConstruction(floorCeilingId,envelopeWithGroundFloor,"floorCeling")
        # envelopeWithWindow = self.queryConstruction(windowId,envelopeWithFloorCeiling,"window")

        envelope.exteriorWall.append(Construction.query.filter_by(id=exWallId).first())
        envelope.interiorWall.append(Construction.query.filter_by(id=inWallId).first())
        envelope.roof.append(Construction.query.filter_by(id=roofId).first())
        envelope.groundFloor.append(Construction.query.filter_by(id=groundFloorId).first())
        envelope.floorCeiling.append(Construction.query.filter_by(id=floorCeilingId).first())
        envelope.window.append(Construction.query.filter_by(id=windowId).first())

        print('envelope',envelope)
        current_db_session=db.session.object_session(envelope)

        #FIXME: current_db_session get to None which cause error
        print ('current_db_session',current_db_session)
        current_db_session.add(envelope)
        #db.session.add(construction)
        current_db_session.commit()

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
            material=Material.query.filter_by(id=int(materialId)).first()
            construction.materials.append(material)

        for tagId in tagIds:
            tag=Tag.query.filter_by(id=int(tagId)).first()
            construction.tags.append(tag)
        
        #reference: https://stackoverflow.com/questions/24291933/sqlalchemy-object-already-attached-to-session
        current_db_session=db.session.object_session(construction)
        current_db_session.add(construction)
        current_db_session.commit()
        #db.session.add(construction)
        #db.session.commit()
        return construction
    
    def update(self,id,name,description,materialIds,thickness,tagIds,categories):
        construction=db.session.query(Construction).filter_by(id=id).first()

        construction.name=name
        construction.description=description
        construction.categories=categories
        construction.thickness=thickness
        construction.materials=[]
        construction.tags=[]
        for materialId in materialIds:
            material=db.session.query(Material).filter_by(id=int(materialId)).first()
            construction.materials.append(material)

        for tagId in tagIds:
            tag=Tag.query.filter_by(id=int(tagId)).first()
            construction.tags.append(tag)
        db.session.commit()
        return construction

    def retrieve(self):
        def retrieve_materials(construction):
            materials=[]
            for material in construction.materials:
                temp = {}
                temp['id'] = str(material.id)
                temp['name'] = material.name
                temp['description'] = material.description
                temp['conductivity'] = material.conductivity
                temp['specificHeat'] = material.specificHeat
                temp['density'] = material.density

                #TODO: table構造を修正してここを直す必要
                if material.classification is None:
                    temp['classification'] = 1
                else:
                    temp['classification'] = material.classification
                materials.append(temp)
            return materials

        def retrieve_tags(construction):
            tags=[]
            for tag in construction.tags:
                temp = {}
                temp['id'] = str(tag.id)
                temp['name'] = tag.name
                tags.append(temp)
            return tags
        
        data = Construction.query.all()
        res = []
        for construction in data:
            temp = {}
            temp['id'] = str(construction.id)
            temp['name'] = construction.name
            temp['description'] = construction.description
            temp['category'] = construction.categories
            temp['materials'] = retrieve_materials(construction)
            temp['tags'] = retrieve_tags(construction)

            thicknessList = construction.thickness.split(",")
            temp["thickness"] = list(map(float, thicknessList))
            
            res.append(temp)
        return res

class MaterialTable():
    def insert(self,name,description,conductibity,specificHeat,density,moistureConductivity,moistureCapacity,classification):
        p=Material(
            name,
            description,
            conductibity,
            specificHeat,
            density,
            moistureConductivity,
            moistureCapacity,
            classification
        )
        db.session.add(p)
        db.session.commit()

        return p

    def update(self,id,name,description,conductibity,specificHeat,density,moistureConductivity,moistureCapacity,classification):
        #p=Material.query.filter_by(id=id).first()
        p=db.session.query(Material).filter_by(id=id).first()
        p.name=name
        p.description=description
        p.conductivity=conductibity
        p.specificHeat=specificHeat
        p.density=density
        p.moistureConductivity=moistureConductivity
        p.moistureCapacity=moistureCapacity
        p.classification=classification
        db.session.commit()

        return p

    def retrieve(self):
        data=Material.query.all()
        res=[]

        for project in data:
            temp={}
            temp["id"]=str(project.id)
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

    