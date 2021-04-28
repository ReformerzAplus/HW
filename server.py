from flask import Flask
from flask import request
app = Flask(__name__)

from pymongo import MongoClient

#登入MongoDB
client = MongoClient()
client = MongoClient('mongodb://admin:admin@localhost:27017/?authSource=admin')

#進入DB
db = client.hw_2_591

#進入Collection
collection = db.house_info

# 【男生可承租】且【位於新北】的租屋物件
# curl "http://localhost:5000/room?location=NewTaipeiCity&gender=male"
@app.route('/room')
def getRoom():
    location = request.args.get('location')
    gender = request.args.get('gender')
    print(request.args)
    
    queryLocation = "新北市"
    querySex = "女生"
    
    if gender == "female":
        querySex = "女生"
    else:
        querySex = "男生"
    if location == "Taipei":
        queryLocation = "台北市"
    else:
        queryLocation = "新北市"

    result = []
    print(queryLocation)
    print(querySex)
    for room in collection.find({"location": queryLocation, "Sex": querySex}):
        result.append(room)
    return str(result)

# 以【聯絡電話】查詢租屋物件
# curl "http://localhost:5000/phone/0900-300-316"
@app.route('/phone/<phone>')
def getPhone(phone):
    result = []
    for room in collection.find({"Phone": phone}):
        result.append(room)
    return str(result)

# 所有【非屋主自行刊登】的租屋物件
# curl "http://localhost:5000/room/owner?owner=False"      查詢非屋主之刊登資訊
# curl "http://localhost:5000/room/owner?owner=True"       查詢屋主之刊登資訊
@app.route('/room/owner')
def owner():
    owner = request.args.get('owner', default = "", type = str)
    ownerQuery = "非屋主"
    if owner == "True":
        ownerQuery = "屋主"
    result = []
    for room in  collection.find({"HouseOwner_author": ownerQuery}):
        result.append(room)
    return str(result)


#【臺北】【屋主為女性】【姓氏為吳】所刊登的所有租屋物件
#curl "http://localhost:5000/room/select?location=Taipei&owner=MissWu1"
#curl "http://localhost:5000/room/select?location=Taipei&owner=MissWu2"
#curl "http://localhost:5000/room/select?location=Taipei&owner=MissWu3"
@app.route('/room/select')
def select():
    location = request.args.get('location', default = "", type = str)
    owner = request.args.get('owner', default = "", type = str)
    print(request.args)
    queryLocation = "新北市"
    queryowner = ""
    if location == "Taipei":
        queryLocation = "台北市"
    if owner == "MissWu1":
        queryowner = "吳小姐"
    if owner == "MissWu2":
        queryowner = "吳媽媽"
    if owner == "MissWu3":
        queryowner = "吳阿姨"
    if owner == "MissWu4":
        queryowner = "吳太太"

    result = []
    print(queryLocation)
    print(queryowner)
    for room in collection.find({"location":queryLocation,"HouseOwner" : queryowner}):
        result.append(room)
    return str(result)
    


#$ export FLASK_APP=server.py
#$ python -m flask run
# * Running on http://127.0.0.1:5000/