from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns=[
    path('home', views.index, name='home'),
    path('register',views.register,name='register'),
    path('login', views.loginform,name='login'),
    path('logout', views.logout,name='logout'),
    path('contact',views.contact,name='contact'),
    path('runmodel',views.runmodel,name='runmodel'),
    path('record',views.record,name='record'),
    path('save',views.save,name='save'),
]