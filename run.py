from unittest import result
from flask import Flask, json,request,jsonify,abort
import werkzeug
from flask.helpers import make_response
import os
import shutil
import subprocess
import time
import pandas as pd
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from src.database import init_db
from subprocess import Popen, PIPE
import datetime
from src.app import app
from src.parser import MaterialTable, ProjectTable, ResultTable,EnvelopeTable,ConstructionTable, ScheduleTable,TagTable, WindowTable
from src.models.models import Construction, Envelope, Project, Results, Schedule, Tag, Therb, Window,db_session,Material
from flask_cors import CORS
import shutil
from zipfile import ZipFile

HASP_UPLOAD_DIR = "lib/hasp/"
HASP_RUNTIME_DIR = "RunHasp.bat"

THERB_UPLOAD_DIR = "lib/therb/"
THERB_RUNTIME_DIR = "lib/therb/通常THERB.exe"

#frontendからのデータ取得を可能にする
api=Api(app)
CORS(app,supports_credentials=True)

@app.route("/")
def hello_world():
    return "<p>test</p>"

#API endpointの設定
# materialのエンドポイント
class MaterialEndpoint(Resource):

    def post(self):
        payload = request.json
        #TODO: payloadのvalidationが必要
        if payload["name"] == "":
            return {"status":"error","message":"name is required"},400
        if "conductivity" not in payload or "specificHeat" not in payload or "density" not in payload or "classification" not in payload:
            return {"status":"error","message":"conductivity, specificHeat, density is required"},400

        materialTable = MaterialTable()
        data=materialTable.insert(
            payload["name"],
            payload["description"],
            payload["conductivity"],
            payload["specificHeat"],
            payload["density"],
            payload["moistureConductivity"],
            payload["moistureCapacity"],
            payload["classification"]
        )

        return {
            "status":"success",
            "message":"could save material",
            "data":{
                "id":str(data.id),
                "name":data.name,
                "description":data.description,
                "conductivity":data.conductivity,
                "specificHeat":data.specificHeat,
                "density":data.density,
            }
        }

    def put(self):
        
        payload = request.json
        if payload["name"] == "":
            return {"status":"error","message":"name is required"},400
        if "conductivity" not in payload or "specificHeat" not in payload or "density" not in payload or "classification" not in payload:
            return {"status":"error","message":"conductivity, specificHeat, density is required"},400

        id = request.args.get('id')
        materialTable = MaterialTable()
        data=materialTable.update(
            id,
            payload["name"],
            payload["description"],
            payload["conductivity"],
            payload["specificHeat"],
            payload["density"],
            payload["moistureConductivity"],
            payload["moistureCapacity"],
            payload["classification"]
        )

        return {
            "status":"success",
            "message":"could update material",
            "data":{
                "id":str(data.id),
                "name":data.name,
                "description":data.description,
                "conductivity":data.conductivity,
                "specificHeat":data.specificHeat,
                "density":data.density,
            }
        }

    def get(self):
        materialTable=MaterialTable()
        return jsonify({
            "status":"success",
            "message":"could retrieve materials",
            "data":materialTable.retrieve()
            })

    def delete(self):
        id = request.args.get('id')
        db=SQLAlchemy()
        material=db.session.query(Material).filter(Material.id==id)
        if material.count() >= 1:
            db.session.delete(material.first())
            db.session.commit()

            return {"status":"success"},200
        else:
            abort(404)

class EnvelopeEndpoint(Resource):
    def post(self):
        payload = request.json
        envelopeTable = EnvelopeTable()
        envelopeTable.insert(
            payload["name"],
            payload["description"],
            payload["exteriorWallId"],
            payload["interiorWallId"],
            payload["roofId"],
            payload["groundFloorId"],
            payload["floorCeilingId"],
            payload["windowId"],
        )

        return {"status":"success"},200

    def get(self):
        envelopeTable=EnvelopeTable()
        return jsonify({
            "status":"success",
            "message":"could retrieve envelopes",
            "data":envelopeTable.retrieve()
            })

    def delete(self):
        id = request.args.get('id')
        db=SQLAlchemy()
        envelope=db.session.query(Envelope).filter(Envelope.id==id)
        if envelope.count() >= 1:
            db.session.delete(envelope.first())
            db.session.commit()

            return {"status":"success"},200
        else:
            abort(404)

class ScheduleEndpoint(Resource):
    def post(self):
        print("schedule post")
        payload = request.json
        scheduleTable = ScheduleTable()
        scheduleTable.insert(
            payload["name"],
            payload["description"],
            payload["tagIds"],
            payload["daily"],
            payload["weekly"],
            payload["monthly"]
        )

        return {"status":"success"},200

    def get(self):
        scheduleTable=ScheduleTable()
        return jsonify({
            "status":"success",
            "message":"could retrieve schedules",
            "data":scheduleTable.retrieve()
        })

    def delete(self):
        id = request.args.get('id')
        db=SQLAlchemy()
        schedule=db.session.query(Schedule).filter(Schedule.id==id)
        if schedule.count() >= 1:
            db.session.delete(schedule.first())
            db.session.commit()

            return {"status":"success"},200
        else:
            abort(404)

class WindowEndpoint(Resource):
    def post(self):
        payload = request.json
        windowTable = WindowTable()
        data=windowTable.insert(
            payload["name"],
            payload["description"],
            payload["materialIds"],
            payload["thickness"],
            payload["tagIds"],
            payload["uvalue"],
        )

        return {
            "status":"success",
            "message":"could save window",
            "data":{
                "id":str(data.id),
                "name":data.name,
                "description":data.description,
                "thickness":data.thickness,
                "categories":data.categories,
            }
        }

    def get(self):
        windowTable=WindowTable()
        return jsonify({
            "status":"success",
            "message":"could retrieve windows",
            "data":windowTable.retrieve()
        })

    def delete(self):
        id = request.args.get('id')
        db=SQLAlchemy()
        window=db.session.query(Window).filter(Window.id==id)
        if window.count() >= 1:
            db.session.delete(window.first())
            db.session.commit()

            return {"status":"success"},200
        else:
            abort(404)

class ConstructionEndpoint(Resource):
    def post(self):
        payload = request.json

        #必要な情報が含まれているかどうかチェック
        if payload["name"] == "":
            return {"status":"error","message":"name is required"},400
        if len(payload["materialIds"]) == 0:
            return {"status":"error","message":"at least one material id is required"},400
        if payload["thickness"] == "":
            return {"status":"error","message":"at least one thickness data is required"},400
        if payload["thickness"].count(",")+1 != len(payload["materialIds"]) :
            return {"status":"error","message":"you cannot select same material in one construction"},400
        
        constructionTable = ConstructionTable()
        data=constructionTable.insert(
            payload["name"],
            payload["description"],
            payload["materialIds"],
            payload["thickness"],
            payload["tagIds"],
            payload["category"],
            payload["uvalue"]
        )

        return {
            "status":"success",
            "message":"could save construction",
            "data":{
                "id":str(data.id),
                "name":data.name,
                "description":data.description,
                "thickness":data.thickness,
                "categories":data.categories,
            }
        }

    def put(self):
        payload = request.json

        #必要な情報が含まれているかどうかチェック
        if payload["name"] == "":
            return {"status":"error","message":"name is required"},400
        if len(payload["materialIds"]) == 0:
            return {"status":"error","message":"at least one material id is required"},400
        if payload["thickness"] == "":
            return {"status":"error","message":"at least one thickness data is required"},400
        if payload["thickness"].count(",")+1 != len(payload["materialIds"]) :
            return {"status":"error","message":"you cannot select same material in one construction"},400
        
        id = request.args.get('id')
        constructionTable = ConstructionTable()
        data=constructionTable.update(
            id,
            payload["name"],
            payload["description"],
            payload["materialIds"],
            payload["thickness"],
            payload["tagIds"],
            payload["category"]
        )

        return {
            "status":"success",
            "message":"could update construction",
            "data":{
                "id":str(data.id),
                "name":data.name,
                "description":data.description,
                "thickness":data.thickness,
                "categories":data.categories,
            }
        }

    def get(self):
        constructionTable=ConstructionTable()
        return jsonify({
            "status":"success",
            "message":"could retrieve constructions",
            "data":constructionTable.retrieve()
        })

    def delete(self):
        id = request.args.get('id')
        db=SQLAlchemy()
        construcion=db.session.query(Construction).filter(Construction.id==id)
        if construcion.count() >= 1:
            db.session.delete(construcion.first())
            db.session.commit()

            return {"status":"success"},200
        else:
            abort(404)

class TagEndpoint(Resource):
    def post(self):
        payload = request.json

        if payload["name"] == "":
            return {"status":"error","message":"name is required"},400

        tagTable = TagTable()
        data=tagTable.insert(
            payload["name"],
            payload["description"]
        )

        return {
            "status":"success",
            "message":"could save tag",
            "data":{
                "id":str(data.id),
                "name":data.name,
            }
        }

    def get(self):
        tagTable=TagTable()
        return jsonify({
            "status":"success",
            "message":"could retrieve tags",
            "data":tagTable.retrieve()
        })

    def delete(self):
        id = request.args.get('id')
        db=SQLAlchemy()
        tag=db.session.query(Tag).filter(Tag.id==id)
        if tag.count() >= 1:
            db.session.delete(tag.first())
            db.session.commit()

            return {"status":"success"},200
        else:
            abort(404)

api.add_resource(EnvelopeEndpoint,'/envelopes')
api.add_resource(ConstructionEndpoint,'/constructions')
api.add_resource(WindowEndpoint,'/windows')
api.add_resource(MaterialEndpoint,'/materials')
api.add_resource(ScheduleEndpoint,'/schedules')
api.add_resource(TagEndpoint,'/tags')

# projectListのエンドポイント
class ProjectListEndpoint(Resource):
    def get(self):
        return {"status":"not implemented yet"}

    def delete(self,id):
        projectTable=ProjectTable()
        projectTable.delete(id)
        return {"status":"success"}

# projectのエンドポイント
class ProjectEndpoint(Resource):
    def delete(self,id):
        projectTable=ProjectTable()
        projectTable.delete(id)
        #TODO:projectを消したときに紐づいているresultも消すようにしたい
        return {"status":"success"}

class ResultEndpoint(Resource):
    def get(self,project_id):

        #resultTable=ResultTable()
        #return {"data":resultTable.retrieve(project_id)}
        return {"status":"not implemented yet"}

    def delete(self,project_id):
        resultTable=ResultTable()
        resultTable.delete(project_id)
        # obj=Result.query.filter_by(project_id=project_id).one()
        # db=SQLAlchemy()
        # db.session.delete(obj)
        # db.session.commit()
        return {"status":"success"}

api.add_resource(ProjectListEndpoint,'/projects')
api.add_resource(ProjectEndpoint,'/projects/<id>')
api.add_resource(ResultEndpoint,'/results/<project_id>')

@app.route('/download/<project_name>',methods=['GET'])
def download(project_name):
    response = make_response(jsonify({"data":"download"}))
    #FIXME: pathをproject_nameではなく、project_idにそろえる
    #データをzip化する
    shutil.make_archive(f'data/{project_name}', 'zip', f'data/{project_name}')
    response.data = open(f'data/{project_name}.zip', 'rb').read()
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Disposition'] = 'attachment; filename={project_name}.zip'.format(project_name=project_name)
    return response

def saveFile(source):
    file = source
    fileName = file.filename

    saveFileName = werkzeug.utils.secure_filename(fileName)
    #TODO:ここでdataフォルダに移動すべき
    #file.save(os.path.join(UPLOAD_DIR, saveFileName))
    print('saveFileName: {}'.format(saveFileName))
    file.save(saveFileName)

@app.route('/therb/run',methods=['POST'])
def run_therb():
    dataset = request.files['dataset']
    datasetName = dataset.filename
    #therbをrunする部分は尾崎先生の修正待ち
    folder = "data"
    #zipファイルを保存する
    saveFile(dataset)

    #zipファイルを解凍する
    with ZipFile(datasetName, 'r') as zip:
        zip.extractall(folder)

    shutil.copy("lib/therb/therb.exe",os.path.join("data",datasetName.replace(".zip",""), "therb.exe"))

    #therbシミュレーションを実行する
    p = Popen(os.path.join("data",datasetName.replace(".zip",""), "therb.exe"))
    
    stdout,stderr=p.communicate()
    print('STDOUT: {}'.format(stdout))

    #zipファイルを削除する
    os.remove(datasetName)
    #dataフォルダのデータも削除する
    shutil.rmtree(os.path.join("data",datasetName.replace(".zip","")))

    # p=Project(name=folder)
    # new_path=os.path.join(os.path.join("data/therb",folder))
    # print('new_path',new_path)
    # df=parseTherb(new_path)

    # roomCount=int((len(df.columns)-3)/3)

    # for i in range(1,roomCount+1):
    #     time = df['time'].to_json()
    #     temperature=df[f'room{i}_temperature'].to_json()
    #     relativeHumidity=df[f'room{i}_relative_humidity'].to_json()
    #     absoluteHumidity=df[f'room{i}_absolute_humidity'].to_json()

    #     r=Therb(
    #         time=time,
    #         name=f'room{i}',
    #         temp=temperature,
    #         relHumidity=relativeHumidity,
    #         absHumidity=absoluteHumidity
    #     )

    #     p.therb.append(r)
    #     db_session.add(r)

    # db_session.add(p)
    # db_session.commit()

    return make_response((jsonify({
        'status':'not implemented yet',
    })))

    
def parseTherb(file):
    def setColumn(df):
        roomCount=(len(df.columns)-3)/3
        colName=['month','day','hour']
        for i in range(1,int(roomCount)+1):
            colName.append(f'room{i}_temperature')
            colName.append(f'room{i}_relative_humidity')
            colName.append(f'room{i}_absolute_humidity')

        df.columns=colName

        return df

    def formatData(col):
        temp = int(col)
        if len(str(temp))==1:
            return '0'+str(temp)
        else:
            return str(temp)

    def date_parser(x):
        return f'{formatData(x.month)}/{formatData(x.day)}/{formatData(int(x.hour))}:00'
        #return datetime.datetime.strptime(f'{formatData(x.month)}/{formatData(x.day)}/{formatData(int(x.hour)-1)}','%m/%d/%H')
    
    outputFile='data/therb/test/o.dat'
    df=pd.read_csv(outputFile,delim_whitespace=True,header=None)
    df = setColumn(df)
    #TODO:flexibleなロジックにすべき
    df = df[:8641]
    df['time']=df.apply(date_parser,axis=1)
    
    return df

@app.route('/run/hasp',methods=['POST'])
def upload_multipart():
    if 'file' not in request.files:
        return make_response(jsonify({'result':'file is required in form data.'}))
    
    saveFile(request.files['file'])
    
    #batchファイルをrunする
    p = Popen(os.path.join(os.getcwd(), HASP_RUNTIME_DIR))
    
    stdout,stderr=p.communicate()
    print('STDOUT: {}'.format(stdout))

    #dataのほうにファイルを移動する
    folder=request.form.get('name')
    
    #フォルダ名が既にあるか確認必要
    new_path=os.path.join(os.path.join("data",folder))

    #awaitする必要あり
    time.sleep(3)
    if os.path.exists(new_path):
        return make_response(jsonify({'message':'error. file name is duplicated. Please change file name.'}))
        #TODO:名前を変えてファイルを保存する方法必要
    else:
        os.makedirs(new_path)
        shutil.move("input001.txt",os.path.join("data",folder, "input001.txt"))
        shutil.move("out20.datweath.dat",os.path.join("data",folder, "out20.datweath.dat"))

        p=Project(name=folder)

        roomId=1
        roomExist=True
        while roomExist:
            #FIXME:ファイルの命名規則を理解してここのロジックをブラッシュアップする必要
            #output_file1='out20.dat___{}.csv'.format(i)
            output_file1='out20.datS__{}.csv'.format(roomId)
            print ('output_file1',output_file1)
            try:     
                #データをparseして、データベースに保存する   
                df1=pd.read_csv(output_file1)
                roomT=df1["ROOM-T"].to_json()
                #print('roomT',roomT)
                clodS=df1["CLOD-S"].to_json()
                rhexS=df1["RHEX-S"].to_json()
                ahexS=df1["AHEX-S"].to_json()
                fs=df1["FS"].to_json()
                roomH=df1["ROOM-H"].to_json()
                clodL=df1["CLOD-L"].to_json()
                rhexL=df1["RHEX-L"].to_json()
                ahexL=df1["AHEX-L"].to_json()
                fl=df1["FL"].to_json()
                mrt=df1["MRT'"].to_json()

                #時間を計算する
                month=df1["MO"].tolist()
                day=df1["DY"].tolist()
                hour=df1["HR"].tolist()
                #print('month',month)
                timeData={}
                for i in range(len(month)):
                    #timeseriesデータはjson serializableじゃない
                    #timeData[i]=datetime.datetime(2021,month[i],day[i],hour[i]-1)
                    timeData[i]=f'2021/{str(month[i])}/{str(day[i])} {str(hour[i])}:00'

                #r=resultTable.insert(roomT,clodS,rhexS,ahexS,fs,roomH,clodL,rhexL,ahexL,fl,mrt)
                r=Results(hour=timeData,roomT=roomT,clodS=clodS,rhexS=rhexS,ahexS=ahexS,fs=fs,roomH=roomH,clodL=clodL,rhexL=rhexL,ahexL=ahexL,fl=fl,mrt=mrt)
                print ('r',r.project_id)
                p.results.append(r)
                db_session.add(r)
         
                shutil.move(output_file1,os.path.join("data",folder, output_file1))
                roomId+=1
            except:
                roomExist=False

        db_session.add(p)
        db_session.commit()

    return make_response((jsonify({
        'status':'success',
        'url':f'http://localhost:8000/{str(r.project_id)}/timeseries'
        })))

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)
    #app.run(debug=True,host='0.0.0.0')