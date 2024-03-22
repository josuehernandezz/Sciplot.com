from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index', views.index, name='index'),
    path('abspl', views.abspl, name='abspl'),
    path('pxrd', views.xrd, name='xrd'),
    path('ftir', views.ftir, name='ftir'),
    path('plqy', views.plqy, name='plqy'),
    path('universal', views.universal, name='universal'),
]
