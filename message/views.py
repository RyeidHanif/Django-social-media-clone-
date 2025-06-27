from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def chat_with(request , reciever_id):
    return HttpResponse("Welcome to your chat with  x reciever ")


def viewcontacts(request):
    return HttpResponse("here are all your contacts ")


def  viewuser(request , userID):
    return HttpResponse("here is the users whatever")


