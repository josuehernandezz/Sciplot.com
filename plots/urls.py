from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('abspl', views.abspl, name='abspl'),
    path('pxrd', views.xrd, name='xrd'),
]
