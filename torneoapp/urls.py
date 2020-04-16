from django.urls import path, URLPattern, URLResolver
from django.conf.urls import url, include
from torneoapp.views import  Home,registroUsuario
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('main/home',views.Home,name='home'),
    path('registro',views.registroUsuario,name='registro'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('add/<str:model>',views.add,name='add'),
    path('addid/<str:model>/<str:id>',views.addid,name='addid'),
    path('listar/<str:model>',views.listar,name='listar'),
    path('listarid/<str:model>/<str:id>',views.listarid,name='listarid'),
    path('modify/<str:model>/<str:id>',views.modify,name='modify'),
    path('partido/<str:id>',views.partido,name='partido'),
    path('delete/<str:model>/<str:id>',views.delete,name='delete'),
    path('deleteid/<str:model>/<str:id>/<str:idmol>',views.deleteid,name='deleteid'),
]