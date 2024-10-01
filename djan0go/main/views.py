import django
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, models
from django.views.decorators.csrf import csrf_protect


api_keys = {
    'testme45' : 'Test_Auth_App'
}

links_auth_client = {}
links_auth_server = {}
serv_tm_api_keys = {}


def index(request):
    print(request.user)
    data = {'version':str(django.get_version())}
    return render(request, 'index.html', context=data)


def my(request):
    print(request.user)
    us = str(request.user)
    if us != 'AnonymousUser':
        return render(request, 'my.html')

    else:
        return redirect('login')

def postuser(request):
    # получаем из данных запроса POST отправленные через форму данные
    name = request.POST.get("name", "Undefined")
    age = request.POST.get("age", 1)
    return HttpResponse(f"<h2>Name: {name}  Age: {age}</h2>")
@csrf_protect
def user_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('my')

    return render(request, 'login.html')
@csrf_protect
def user_logout(request):
    logout(request)
    if 1 == 1:
        return redirect('login')



def get_urls_api(request, api_key):
    if api_key in api_keys:
        nm1 = str(random.randint(1000000, 99999999))
        nm2 = str(random.randint(1000000, 99999999))

        cl = f'https://cubefel.ru/cfa/client_fw/{nm1}'
        srv = f'https://cubefel.ru/cfa/server_code_ch/{nm2}'

        links_auth_client[nm1] = api_keys[api_key]
        links_auth_server[nm2] = {'code':0, 'login':'&?'}
        serv_tm_api_keys[nm1] = nm2
        print(links_auth_server)
        print(links_auth_client)
        return JsonResponse({'client_url':cl, 'server_code_ch':srv})
    else:
        return JsonResponse({'code':'403'})


def server_code_ch(request, tm_api_key):
    if tm_api_key in links_auth_server:

        return JsonResponse({'code' : links_auth_server[tm_api_key]['code'], 'login' : links_auth_server[tm_api_key]['login']})

def client_fw(request, tm_api_key):
    if tm_api_key in links_auth_client:
        us = str(request.user)
        if us != 'AnonymousUser':
            print('hello')
            appname = links_auth_client[tm_api_key]
            return HttpResponse(f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Подтверждение авторизации CFA</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>


<div class="container">
    <div class="mb-3">

        <h4>ㅤ</h4>


    
    
    <h3>ㅤ</h3>
    <div class="card">
  <div class="card-header">
    CubeFel Account Авторизация
  </div>
  <div class="card-body">
<h1"><picture>  <img src="https://img1.picmix.com/output/stamp/normal/6/7/5/5/1475576_7f8e6.gif" alt="Sweeper" style="margin-left: 16px;" data-astro-cid-sr76vcv2="" width="130" height="130" loading="lazy" decoding="async"> </picture></h1>
    <h5 class="card-title">Авторизация в приложении "{appname}"</h5>
    <p class="card-text">Приложение "{appname}" получит ваш логин. Вы будете авторизованы как {request.user}</p>
    <a href="https://cubefel.ru/cfa/complete_auth/{tm_api_key}" class="btn btn-success">Подтверждаю авторизацию</a>
  </div>

</div>
    </div>

</body>
</html>''')
        else:
            return HttpResponse('Для начала авторизуйтесь на https://cubefel.ru/cfa/login и попробуйте ещё раз')

    else:
        return JsonResponse({'code': '403'})


def complete_auth(request, tm_api_key):
    if tm_api_key in links_auth_client:
        nm2 = serv_tm_api_keys[tm_api_key]
        links_auth_server[nm2]['code'] = 1
        links_auth_server[nm2]['login'] = str(request.user)
        return render(request, 'success.html')
    else:
        return JsonResponse({'code': '403'})

def hi_tester(request):
    if 1 == 1:
        return HttpResponse("""
<html lang="en"><head>
    <meta charset="UTF-8">
    <title>Приветственная страница для тестеров</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body style="">

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>


<div class="container">
    <div class="mb-3">


<h1 align="center"><picture>  <img src="https://media1.tenor.com/m/3-v67kKuolwAAAAC/tester.gif" alt="Sweeper" style="margin-left: 16px;" data-astro-cid-sr76vcv2=""> </picture></h1>
<a class="navbar-brand"><h1 align="center">Здравствуй, тестер!</h1></a>
<a class="navbar-brand" href="/logout"></a>

<h3 align="center"><button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasExample" aria-controls="offcanvasExample">
  Меню навигации CFA
</button></h3>

<div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasExample" aria-labelledby="offcanvasExampleLabel">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="offcanvasExampleLabel">Меню навигации CFA</h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <div>Здесь вы можете быстро переходить между страницами.</div><h4>ㅤ</h4>
    
    <h3 align="center"><a href="https://cubefel.ru/cfa/" class="btn btn-primary">Главная страница</a></h3>
    <h3 align="center"><a href="https://cubefel.ru/cfa/my" class="btn btn-primary">Личный кабинет</a></h3>
    <h3 align="center"><a href="https://cubefel.ru/cfa/login" class="btn btn-primary">Меню входа</a></h3>
    <h3 align="center"><a href="https://cubefel.ru/cfa/info" class="btn btn-primary">Инфо о проекте</a></h3>
   <source srcset="https://terminator.aeza.net/_astro/fan.ropKkb2V_1Izs1m.webp" type="image/webp"> <img src="https://terminator.aeza.net/_astro/fan.ropKkb2V_ZBagrK.png" alt="Fan. Just a regular fan. No jokes" style="align-self: flex-end; margin-bottom: 13px; margin-right: 15px;" data-astro-cid-ssfzsv2f="" width="45" height="53" loading="lazy" decoding="async">    
  </div>
</div>

    <h4>ㅤ</h4>
        <div class="row">
    <div class="card text-center">
  <div class="card-header">
    CubeFel Account
  </div>
  <div class="card-body">
    <h5 class="card-title">Сообщение для тестеров</h5>
    <p class="card-text">Сначало нужно войти в свой аккаунт, который выдал админ. Дальше проверить всё страницы вплоть до мелочный кнопок. В случае обнаружения багов, недочётов итд. свяжитесь с разработчиком. Все страницы вы можете найти в меню навигации.</p>
    
  </div>
  <div class="card-footer text-body-secondary">...</div>
</div>
<h3>ㅤ</h3>


    </div>
    </div>


</div><deepl-input-controller></deepl-input-controller></body></html>""")
    else:
        return HttpResponse("Для тестирования системы авторизации нужно войти в систему")




def testapp_pg(request):
    us = str(request.user)
    if us != 'AnonymousUser':
        return HttpResponse("""
        <html lang="en"><head>
    <meta charset="UTF-8">
    <title>Тестирование авторизации CFA</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body style="">

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>


<div class="container">
    <div class="mb-3">


<h1 align="center">ㅤ</h1>
    <h1 align="center">ㅤ</h1>
<a class="navbar-brand"><h1 align="center">Тестирование авторизации в сторонних приложениях</h1></a>


<h3 align="center"><button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasExample" aria-controls="offcanvasExample">
  Меню навигации CFA
</button></h3>
<h4 align="center">ㅤ</h4>
<div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasExample" aria-labelledby="offcanvasExampleLabel">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="offcanvasExampleLabel">Меню навигации CFA</h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <div>Здесь вы можете быстро переходить между страницами.</div><h4>ㅤ</h4>
    
    <h3 align="center"><a href="https://cubefel.ru/cfa/" class="btn btn-primary">Главная страница</a></h3>
    <h3 align="center"><a href="https://cubefel.ru/cfa/my" class="btn btn-primary">Личный кабинет</a></h3>
    <h3 align="center"><a href="https://cubefel.ru/cfa/login" class="btn btn-primary">Меню входа</a></h3>
    <h3 align="center"><a href="https://cubefel.ru/cfa/info" class="btn btn-primary">Инфо о проекте</a></h3>
   <source srcset="https://terminator.aeza.net/_astro/fan.ropKkb2V_1Izs1m.webp" type="image/webp"> <img src="https://terminator.aeza.net/_astro/fan.ropKkb2V_ZBagrK.png" alt="Fan. Just a regular fan. No jokes" style="align-self: flex-end; margin-bottom: 13px; margin-right: 15px;" data-astro-cid-ssfzsv2f="" width="45" height="53" loading="lazy" decoding="async">    
  </div>
</div>

    <h4 align="center"><p>В коде страницы никак не связаны. Используются только GET запросы.</p></h4>
  
<h3 align="center"><a href="https://cubefel.ru/cfa/testapp_auth" class="btn btn-warning">Начать</a></h3>
    </div>


</div><deepl-input-controller></deepl-input-controller></body></html>""")
    else:
        return HttpResponse("Для тестирования системы авторизации нужно войти в систему")


def info(request):
    return render(request, "info.html")