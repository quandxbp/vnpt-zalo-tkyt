from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tkyt', views.tkyt, name='tkyt'),
    path('follow_hook', views.follow_hook, name='follow_hook')
]