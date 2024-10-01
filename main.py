# demo of auth
import time
import webbrowser
import requests as rq

input('для начала авторизации нажмите enter')

urls = rq.get('http://127.0.0.1:8000/get_urls_api/testme45')
cont = urls.json()
webbrowser.open(cont['client_url'])

while True:
    d = rq.get(cont['server_code_ch'])
    contt = d.json()

    if contt['code'] == 1:
        print(f'Успешная авторизация! Получен логин: {contt["login"]}')
        break

    time.sleep(3)

