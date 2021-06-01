from django.shortcuts import render
from .models import destination

def index(request):

    dests=destination.objects.all()
    return render(request,'index.html',{'dests':dests})