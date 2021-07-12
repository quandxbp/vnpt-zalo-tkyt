from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('message', views.message, name='message'),
    path('test', views.test, name='test'),
    path('follow_hook', views.follow_hook, name='follow_hook')
]