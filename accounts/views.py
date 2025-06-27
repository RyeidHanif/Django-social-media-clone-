from django.shortcuts import render , redirect 
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib import messages 



# Create your views here.


def signup(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request , "Signed up Successfully . Please login now ")
            return redirect("login")
        else :
            messages.warning(request, "form is not valid , please refill it ")
            return render(request, "accounts/signup.html", {"form": register_form})
    else : 
        register_form  = RegisterForm()
    
    return render(request, "accounts/signup.html", {"form" : register_form})


            
    
    
