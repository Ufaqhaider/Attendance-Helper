from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.http import HttpResponse
def home(request):
    return render(request,'Home.html')  #yaha render mtlb kisi dusri file ko call krna

def contact(request):
    return HttpResponse("<h1>contact<h1>")


def add(request):

    val1=int(request.POST["num1"])
    val2=int(request.POST["num2"])
    res=val1+val2
    return render(request,'result.html',{"result":res})