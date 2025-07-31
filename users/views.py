from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import CustomRegistrationForm
# Create your views here.
def sign_up(request):
    if request.method=='POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print('form is not valid')
    return render(request, 'registration/register.html',{"form":form})

def login(request):
    pass