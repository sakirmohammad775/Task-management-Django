from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
   return HttpResponse('hello i am back')

def contact(request):
    return HttpResponse('contact me')

def show_task(request):
    return HttpResponse('This is our task page')