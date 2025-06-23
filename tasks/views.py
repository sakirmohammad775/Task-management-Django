from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
   return HttpResponse('contact me')

def manager_dashboard(request):
    return render(request, 'dashboard/manager_dashboard.html')

def user_dashboard(request):
    return render(request, 'dashboard/user_dashboard.html')

def test(request):
    context={
        'names':['John',"ahmed","john"],
        'age':[25,30,35],
        'city':['cairo','alex','giza']
        
    }
    return render(request,'test.html',context)