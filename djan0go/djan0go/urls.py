"""
URL configuration for djan0go project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views

cfa = [
path('admin/', admin.site.urls),
    path('', views.index, name='main_page'),
    path('postuser/', views.postuser),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('my/', views.my, name='my'),
    path("get_urls_api/<str:api_key>", views.get_urls_api),
    path("server_code_ch/<str:tm_api_key>", views.server_code_ch),
    path("client_fw/<str:tm_api_key>", views.client_fw),
    path("complete_auth/<str:tm_api_key>", views.complete_auth),
    path("hi_tester/", views.hi_tester),
    path("testapp/", views.testapp_pg),
    path("info/", views.info),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cfa/', include(cfa))
]