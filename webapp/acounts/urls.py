from django.urls import path
from . import views #here . means all
from django.http import HttpResponse





urlpatterns = [
    path('',views.home),
    path('contact',views.contact),
    path('add',views.add)
]