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

# curl localhostt:5000/room?location=newTaipei&gender=male
@app.route('/room')
def getRoom():
    # male/female
    gender = request.args.get('gender')
    # newTaipei/Taipei
    location = request.args.get('location')
    querySex = "男生"
    queryLocation = "新北市"
    if location == "Taipei":
        queryLocation = "台北市"
    if gender == "female":
        querySex = "女生"
    result = []
    print(queryLocation)
    print(querySex)
    for room in collection.find({"location": queryLocation, "Sex": querySex}):
        result.append(room)
    return str(result)

# 3
# /phone/0911-111-111
@app.route('/phone/<phone>')
def getPhone(phone):
    result = []
    for room in collection.find({"Phone": phone}):
        result.append(room)
    return str(result)

# 4
# /notOwner/非屋主
# curl localhostt:5000/room/owner?owner=False
# curl localhostt:5000/room/owner?owner=True
# 
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



#   1.【設計/建立 RESTful API】供查詢下列資訊: 【以 JSON 格式回傳，請自訂 Schema】
# - 2. 【男生可承租】且【位於新北】的租屋物件, gender=male&location=newTaipei
# - 3. 以【聯絡電話】查詢租屋物件, phone= 
# - 4. 所有【非屋主自行刊登】的租屋物件  byOwner=False
# - 5. 【臺北】【屋主為女性】【姓氏為吳】所刊登的所有租屋物件 location=,owner_gender=,owner_name

#$ export FLASK_APP=server.py
#$ python -m flask run
# * Running on http://127.0.0.1:5000/