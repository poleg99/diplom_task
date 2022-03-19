import re, os
import requests
import mysql.connector
import datetime
import json
from requests.structures import CaseInsensitiveDict
from lxml import etree as etree
from decimal import Decimal

conn = mysql.connector.connect(user='root',
                               password='pass',
                               host='127.0.0.1',
                               database='metalsdb',
                               auth_plugin='mysql_native_password')

if conn:
    print ("Connected Successfully")
else:
    print ("Connection Not Established")


#url = "http://www.cbr.ru/scripts/xml_metall.asp?date_req1=01/08/2001&date_req2=13/08/2001"
#url = "http://api.nbp.pl/api/cenyzlota/2013-01-01/2013-01-31/"
# as CBR add captcha for it's site, I created CBR emulator
url = "http://cbr.example.com/metals.xml"

headers = {'User-Agent': 'Mozilla',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-encoding': 'none',
         'Connection': 'keep-alive',
         'Content-Type': 'application/xml; charset=windows-1251',
         'content-Encoding': 'gzip'}

resp = requests.get(url,timeout=3,headers=headers)

if resp.status_code == requests.codes.ok:
    root = etree.fromstring(resp.content)

    for child in root:
        dt = child.attrib.get('Date')
        code = child.attrib.get('Code')

        for elem in child.getchildren():
            if not elem.text:
                text = "None"
            else:
                text = elem.text
                if elem.tag =="Buy":
                    buy = elem.text
                if elem.tag == "Sell":
                    sell = elem.text

        print(dt + "," +code +"," + buy.replace(',','.') +"," + sell.replace(',','.'))

        cursor = conn.cursor()
#        metalsdata = """REPLACE INTO metals_data (dt,code,buy,sell) VALUES (STR_TO_DATE(%s,'%d.%m.%Y'),%s,%s,%s)"""
        metalsdata = "SELECT * from metalsdb.metalls_v"
        cursor.execute(metalsdata)
#        conn.commit()
        metals_data = cursor.fetchall()
        json_data=[]
        for result in metals_data:
          json_data.append(dict(zip(row_headers,result)))
        return json.dumps(json_data)
        print("Data inserted successfully.")
else:
    print('Failed to upload xml. Error code=' + str(resp.status_code))
