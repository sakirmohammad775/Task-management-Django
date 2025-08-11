from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import CustomRegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


# Create your views here.(first)
# def sign_up(request):
#     if request.method == "POST":
#         form = CustomRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#         else:
#             print("form is not valid")
#     else:
#         form = CustomRegistrationForm()
#     return render(request, "registration/register.html", {"form": form})


## after module 11.5
def sign_up(request):
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print("user", user)
            user.set_password(form.cleaned_data.get("password1"))
            print(form.cleaned_data)
            user.is_active = False
            user.save()
            messages.success(
                request, "A Confirmation mail sent.Please check your email"
            )
            return redirect("sign-in")
        else:
            print("form is not valid")
            print(form.errors.as_json())
    else:
        form = CustomRegistrationForm()
    return render(request, "registration/register.html", {"form": form})


def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("Doc", username, password)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "registration/login.html",
                {"error": "invalid username or password"},
            )
    return render(request, "registration/login.html")


def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign-in")
