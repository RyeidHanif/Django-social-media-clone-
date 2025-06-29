from django.shortcuts import render , redirect 
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib import messages 
from post.models import ProfilePhoto



# Create your views here.


def signup(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        photo= request.FILES.get("photo")
        if register_form.is_valid():
            user= register_form.save()
            ProfilePhoto.objects.create(user=user, photo=photo)
            messages.success(request , "Signed up Successfully . Please login now ")
            return redirect("login")
  
    else : 
        register_form  = RegisterForm()
    
    return render(request, "accounts/signup.html", {"form" : register_form})


            
    
    
