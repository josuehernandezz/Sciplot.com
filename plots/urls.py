from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('abspl', views.abspl, name='abspl'),
    path('pxrd', views.xrd, name='xrd'),
    path('update_title', views.update_title, name='update_title'),
    # path('homepage', views.homepage, name='homepage'),
    path('plot', views.plot, name='plot'),
]
