from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
import json
from pymongo import MongoClient

#登入MongoDB
client = MongoClient()
client = MongoClient('mongodb://admin:admin@localhost:27017/?authSource=admin')

#進入DB
db = client.hw_2_591

#進入Collection
collection = db.house_info

def insertData(data):
    collection.insert_one(data)

def getAllData(url):
    totalPage = driver.execute_script("return document.querySelectorAll('.pageBar a.pageNum-form')[5].text")
    for page in range(int(totalPage)):
        elementA = driver.execute_script("return document.querySelectorAll('.listInfo h3 a')")
        print("總頁數：",totalPage)
        print("目前頁數：",page+1)
        links = []
        for a in elementA:
            links.append(a.get_attribute('href'))
        print(links)

        #抓取資料
        for link in links:
            strScript = 'window.open("'+link+'")'
            driver.execute_script(strScript)
            sleep(1) # seconds
            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            
            ###地區
            location = driver.execute_script("return document.querySelectorAll('#propNav a')[2].innerText")

            ###出租者
            owner = driver.execute_script("return document.querySelector(\".avatarRight div i\").innerText")
           
            ###出租者身份
            author = (driver.execute_script("return document.querySelector('.avatarRight div').innerText")).split()[1]
            is_Owner = re.search('(屋主)',author)

            ###聯絡電話
            phone = driver.execute_script('return document.querySelector(".dialPhoneNum").getAttribute("data-value")')
            
            ###房屋型態：
            search_house_type = (driver.execute_script("return document.querySelector('.attr').innerText"))
            house_type = re.search('(透天厝)|(電梯大樓)|(公寓)',search_house_type)

            ###現況
            search_now_type = (driver.execute_script("return document.querySelector('.attr').innerText"))
            now_type = re.search('(分租套房)|(整層住家)|(車位)|(獨立套房)|(雅房)|(其他)',search_house_type)

            ###性別要求
            search_male_or_female_type = (driver.execute_script("return document.querySelector('ul.clearfix.labelList.labelList-1').innerText"))
            sex_type = re.search('(男女生皆可)|(男生)|(女生)',search_male_or_female_type)

            ht = house_type.group(0) if house_type is not None else None
            st = sex_type.group(0) if sex_type is not None else None
            nt = now_type.group(0) if now_type is not None else None
            nr = is_Owner.group(0) if is_Owner is not None else "非屋主"
            
            data = {"location": location , "HouseOwner": owner , "HouseOwner_author": nr , "Phone": phone , "House_Type": ht , "Now_Type": nt , "Sex": st}
            print(data)
            insertData(data)
          
            ###關閉分頁
            driver.close()
            driver.switch_to.window(windows[0])
            sleep(1) # seconds
        
        #換到下一頁
        driver.execute_script("document.querySelector('.pageBar a.pageNext').click()")
        sleep(.8) #seconds

#開啟瀏覽器Chrome
chrome_options = Options() # 啟動無頭模式
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome("/Users/ReformerzAplus/project_2/chromedriver", options=chrome_options)
url = "https://rent.591.com.tw/?kind=0&region=1"
driver.get(url)
sleep(1) # seconds

#點擊地區（台北）
#Taipei = driver.execute_script("document.querySelector(\"[data-id='1']\").click()")
NewTaipeiCity = driver.execute_script("document.querySelector(\"[data-id='3']\").click()")
sleep(1) # seconds

# options = webdriver.ChromeOptions()
# prefs = {
#     'profile.default_content_setting_values' :
#         {
#         'notifications' : 2
#         }
# }
# options.add_experimental_option('prefs',prefs)

#getAllData(Taipei)
getAllData(NewTaipeiCity)
