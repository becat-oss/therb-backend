#from sqlalchemy import *

import sqlalchemy as sa
from sqlalchemy.orm import (backref,scoped_session,sessionmaker,relationship)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta
from src.config import Config
from src.database import db 
#from src.app import db

engine = sa.create_engine(Config.SQLALCHEMY_DATABASE_URI,convert_unicode=True)

Base:DeclarativeMeta = declarative_base()
Base.metadata.bind = engine

db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base.query = db_session.query_property()

construction_material = db.Table('construction_material',
    db.Column('constructionId',db.Integer,db.ForeignKey('construction.id')),
    db.Column('materialId',db.Integer,db.ForeignKey('material.id')),
)

construction_tag = db.Table('construction_tag',
    db.Column('constructionId',db.Integer,db.ForeignKey('construction.id')),
    db.Column('tagId',db.Integer,db.ForeignKey('tag.id')),
)

class Material(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False,unique=True)
    description = db.Column(db.String(255),nullable=False)
    conductivity = db.Column(db.Float,nullable=False)
    specificHeat = db.Column(db.Float,nullable=False)
    density = db.Column(db.Float,nullable=False)
    moistureConductivity = db.Column(db.Float,nullable=False)
    moistureCapacity = db.Column(db.Float,nullable=False)
    classification = db.Column(db.Integer,nullable=True)
    #constructionId = db.Column(db.Integer,db.ForeignKey('construction.id'),nullable=True)

    def __init__(self,name,description,conductivity,specificHeat,density,moistureConductivity,moistureCapacity,classification):
        self.name = name
        self.description = description
        self.conductivity = conductivity
        self.specificHeat = specificHeat
        self.density = density
        self.moistureConductivity = moistureConductivity
        self.moistureCapacity = moistureCapacity
        self.classification = classification

    def toDict(self):
        if self.classification is None:
            classification = 1
        else:
            classification = self.classification

        return{
            'id':str(self.id),
            'name':self.name,
            'description':self.description,
            'conductivity':self.conductivity,
            'specificHeat':self.specificHeat,
            'density':self.density,
            'moistureConductivity':self.moistureConductivity,
            'moistureCapacity':self.moistureCapacity,
            'classification':classification
        }

exWallIdentifier = db.Table('exWallIdentifier',
    db.Column('envelopeId',db.Integer,db.ForeignKey('envelope.id')),
    db.Column('exWallId',db.Integer,db.ForeignKey('construction.id')),
)

inWallIdentifier = db.Table('inWallIdentifier',
    db.Column('envelopeId',db.Integer,db.ForeignKey('envelope.id')),
    db.Column('inWallId',db.Integer,db.ForeignKey('construction.id')),
)

roofIdentifier = db.Table('roofIdentifier',
    db.Column('envelopeId',db.Integer,db.ForeignKey('envelope.id')),
    db.Column('roofId',db.Integer,db.ForeignKey('construction.id')),
)

groundFloorIdentifier = db.Table('groundFloorIdentifier',
    db.Column('envelopeId',db.Integer,db.ForeignKey('envelope.id')),
    db.Column('groundFloorId',db.Integer,db.ForeignKey('construction.id')),
)

floorCeilingIdentifier = db.Table('floorCeilingIdentifier',
    db.Column('envelopeId',db.Integer,db.ForeignKey('envelope.id')),
    db.Column('floorCeilingId',db.Integer,db.ForeignKey('construction.id')),
)

windowIdentifier = db.Table('windowIdentifier',
    db.Column('envelopeId',db.Integer,db.ForeignKey('envelope.id')),
    db.Column('windowId',db.Integer,db.ForeignKey('construction.id')),
)

class Envelope(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False,unique=True)
    description = db.Column(db.String(255),nullable=False)
    exteriorWall = db.relationship("Construction",secondary=exWallIdentifier)
    interiorWall = db.relationship("Construction",secondary=inWallIdentifier)
    roof = db.relationship("Construction",secondary=roofIdentifier)
    groundFloor = db.relationship("Construction",secondary=groundFloorIdentifier)
    floorCeiling = db.relationship("Construction",secondary=floorCeilingIdentifier)
    window = db.relationship("Construction",secondary=windowIdentifier)
    #exteriorWall = db.Column(db.Integer,db.ForeignKey('construction.id'))
    #interiorWall = db.Column(db.Integer,db.ForeignKey('construction.id'))

    def __init__(self,name,description):
        self.name = name
        self.description = description

    def toDict(self):
        return{
            'id':str(self.id),
            'name':self.name,
            'description':self.description,
            'exteriorWall':[c.toDict() for c in self.exteriorWall][0],
            'interiorWall':[c.toDict() for c in self.interiorWall][0],
            'roof':[c.toDict() for c in self.roof][0],
            'groundFloor':[c.toDict() for c in self.groundFloor][0],
            'floorCeiling':[c.toDict() for c in self.floorCeiling][0],
            'window':[c.toDict() for c in self.window][0],
        }

class Construction(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False,unique=True)
    description = db.Column(db.String(255),nullable=False)
    materials = db.relationship('Material',secondary=construction_material,backref='constructions')
    thickness = db.Column(db.String(255),nullable=False) # 10,20,10 thickness =10mm,20mm,10mm
    categories =db.Column(db.String(255),nullable=False)
    tags = db.relationship('Tag',secondary=construction_tag,backref='constructions')
    uvalue = db.Column(db.Float,nullable=True)
    #envelopes = db.relationship('Envelope',backref='construction',lazy='dynamic')

    def __init__(self,name,description,categories,thickness,uvalue):
        self.name = name
        self.description = description
        self.categories = categories
        self.thickness = thickness
        self.uvalue = uvalue

    def toDict(self):
        thicknessList = self.thickness.split(",")
        thickness = list(map(float, thicknessList))

        return{
            'id':str(self.id),
            'name':self.name,
            'description':self.description,
            'category':self.categories,
            'materials':[m.toDict() for m in self.materials],
            'tags':[t.toDict() for t in self.tags],
            'thickness':thickness,
            'uvalue':self.uvalue
        }

class Tag(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False,unique=True)
    description = db.Column(db.String(255),nullable=True)
    constructionId = db.Column(db.Integer,db.ForeignKey('construction.id'),nullable=True)
    
    def __init__(self,name,description):
        self.name = name
        self.description = description

    def toDict(self):
        return{
            'id':str(self.id),
            'name':self.name,
        }

class Project(Base):
    __tablename__='project'

    id=sa.Column(sa.Integer, primary_key=True)
    name=sa.Column(sa.String,nullable=False)
    results=relationship('Results',backref='project',lazy=True)
    #therb=relationship('Therb',backref='project',lazy=True)

class Therb(Base):
    __tablename__='therb'
    project_id=sa.Column(sa.Integer,sa.ForeignKey('project.id'),nullable=False)
    id=sa.Column(sa.Integer, primary_key=True)
    name=sa.Column(sa.String,nullable=False)
    time=sa.Column(sa.JSON)
    temp=sa.Column(sa.JSON)
    relHumidity=sa.Column(sa.JSON)
    absHumidity=sa.Column(sa.JSON)

    def serialize(self):
        return{"room":self.temp}

#roomが複数ある場合のテーブル構造を考える必要あり
class Results(Base):
    #1つのroomにつき1つのResult
    __tablename__='result'

    project_id=sa.Column(sa.Integer,sa.ForeignKey('project.id'))
    id=sa.Column(sa.Integer, primary_key=True)
    hour=sa.Column(sa.JSON,nullable=False)
    roomT=sa.Column(sa.JSON,nullable=False)
    clodS=sa.Column(sa.JSON,nullable=False)
    rhexS=sa.Column(sa.JSON,nullable=False)
    ahexS=sa.Column(sa.JSON,nullable=False)
    fs=sa.Column(sa.JSON,nullable=False)
    roomH=sa.Column(sa.JSON,nullable=False)
    clodL=sa.Column(sa.JSON,nullable=False)
    rhexL=sa.Column(sa.JSON,nullable=False)
    ahexL=sa.Column(sa.JSON,nullable=False)
    fl=sa.Column(sa.JSON,nullable=False)
    mrt=sa.Column(sa.JSON,nullable=False)

    def serialize(self):
        return{"room":self.roomT}

# Base.metadata.create_all(engine)

# class Project(db.Model):
#     __tablename__='project'

#     id=db.Column(db.Integer, primary_key=True)
#     name=db.Column(db.String,nullable=False)
#     results=sa.relationship('Result',backref='project',lazy=True)

# #roomが複数ある場合のテーブル構造を考える必要あり
# class Result(sa.Model):
#     #1つのroomにつき1つのResult
#     __tablename__='result'

#     project_id=sa.Column(sa.Integer,sa.ForeignKey('project.id'))
#     id=sa.Column(sa.Integer, primary_key=True)
#     hour=sa.Column(sa.JSON,nullable=False)
#     roomT=sa.Column(sa.JSON,nullable=False)
#     clodS=sa.Column(sa.JSON,nullable=False)
#     rhexS=sa.Column(sa.JSON,nullable=False)
#     ahexS=sa.Column(sa.JSON,nullable=False)
#     fs=sa.Column(sa.JSON,nullable=False)
#     roomH=sa.Column(sa.JSON,nullable=False)
#     clodL=sa.Column(sa.JSON,nullable=False)
#     rhexL=sa.Column(sa.JSON,nullable=False)
#     ahexL=sa.Column(sa.JSON,nullable=False)
#     fl=sa.Column(sa.JSON,nullable=False)
#     mrt=sa.Column(sa.JSON,nullable=False)

#     def serialize(self):
#         return{"room":self.roomT}