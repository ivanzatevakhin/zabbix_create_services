#!/usr/bin/env python3
import requests
import json

ZABBIX_API_URL = "http://127.0.0.1/zabbix/api_jsonrpc.php"
UNAME = "Admin"
PWORD = "admin"

r = requests.post(ZABBIX_API_URL,
                  json={
                        "jsonrpc": "2.0",
                        "method": "user.login",
                        "params": {
                        "user": UNAME,
                        "password": PWORD},
                        "id": 1
                  })

#print(json.dumps(r.json(), indent=4, sort_keys=True))

AUTHTOKEN = r.json()["result"]

mode_1=int(input('Добавить новые сервисы из триггеров - 1; Добавить новый родительский сервис - 2: '))
if mode_1 == 1:
    host_id=input('Введите id Хоста: ')
    z=input('Введите родительский ID Сервиса: ')
    host_des=input('Введите ключ для поиска триггера: ')

    spisok_1 = []
    spisok_2 = ()

    for v in host_des:
        if v[:4] == 'Free':
            print(v)
    r = requests.post(ZABBIX_API_URL,
                json={
                    "jsonrpc": "2.0",
                    "method": "trigger.get",
                    "params": {
                    "output": [
                    "triggerid",
                    "description",
                    "priority"],
                    "hostids" : host_id,
                    "search": {
                    "description": host_des
                    },
                    },
                    "id": 2,
                    "auth": AUTHTOKEN
                })
    data = json.dumps(r.json(), indent=4, sort_keys=True)
    data_1 = json.loads(data)


    for item in data_1['result']:
        x=item['description']
        y=item['triggerid']

        #P=input('Введите id родительского сервиса: ')
        k = requests.post(ZABBIX_API_URL,
                json={
                    "jsonrpc": "2.0",
                    "method": "service.get",
                    "params": {
                    "output":[
                    "serviceid" ,
                    "dependencies"
                    ],
                    "selectDependencies":[
                    "servicedownid",
                    "serviceupid"
                    ],
                    "filter" : {
                        "serviceid": [
                            z
                         ]
                    },
                    },
                    "id": 2,
                    "auth": AUTHTOKEN
                })
        data_rn = json.dumps(k.json(), indent=4, sort_keys=True)
        data_rn_1 = json.loads(data_rn)

        for depend_item_2 in data_rn_1['result'][0]['dependencies']:
            h = depend_item_2['serviceid']
            rm = requests.post(ZABBIX_API_URL,
                json={
                    "jsonrpc": "2.0",
                    "method": "service.get",
                    "params": {
                        "output":[
                        "name",
                        "serviceid"],
                        "filter": {
                        "serviceid" : h
                        },
                    },
                    "id": 2,
                    "auth": AUTHTOKEN
                })
            data_rm = json.dumps(rm.json(), indent=4, sort_keys=True)
            data_rm_1 = json.loads(data_rm)
            h1 = (data_rm_1['result'][0]['name'])
            spisok_1.append(h1)
#        if h1 == [x]:
#            print(x, " - its x")
#            print(spisok_1, " - its h1")
        if  any(x in spisok_2 for spisok_2 in spisok_1)==True:
            print(x, " - this service already exist")
        else :
                r = requests.post(ZABBIX_API_URL,
                  json={
                    "jsonrpc": "2.0",
                    "method": "service.create",
                        "params": {
                        "name":x,
                        "algorithm": 1,
                        "triggerid":y,
                        "showsla": 0,
                        "goodsla": 99.99,
                        "sortorder": 0,
                        "parentid":z
                        },

                      "id": 2,
                      "auth": AUTHTOKEN
                    })
                print(x,"- service created")
else:
    a=input('Введите имя Сервиса: ')
    b=input('Введите родительский ID Сервиса: ')
#           print(type(item['description']))
#           x=item['description']
#           y=item['triggerid']
    r = requests.post(ZABBIX_API_URL,
                  json={
                    "jsonrpc": "2.0",
                    "method": "service.create",
                        "params": {
                        "name":a,
                        "algorithm": 1,
                        "showsla": 0,
                        "goodsla": 99.99,
                        "sortorder": 0,
                        "parentid":b
                        },

                      "id": 2,
                      "auth": AUTHTOKEN
                    })
    print("service has been created")
