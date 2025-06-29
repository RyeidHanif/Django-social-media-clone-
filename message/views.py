from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Messages
from .forms import MessageForm

# Create your views here.


def chat_with(request, reciever_id):
    current_user = request.user
    other_user = User.objects.get(id=reciever_id)
    messages = Messages.objects.filter(
        sender__in=[current_user, other_user], reciever__in=[current_user, other_user]
    ).order_by("timesent")

    if request.method == "POST":
        messageform = MessageForm(request.POST)
        if messageform.is_valid():
            message = messageform.save(commit=False)
            message.sender = request.user
            message.reciever = other_user
            message.save()
            return redirect("chat_with", reciever_id=reciever_id)

    else:
        messageform = MessageForm()

    return render(
        request,
        "message/chatuser.html",
        {"messages_set": messages, "form": messageform, "other_user": other_user},
    )


def viewcontacts(request):
    contacts = User.objects.all()
    if request.method == "POST":
        if request.POST.get("message"):
            return redirect("chat_with", reciever_id=request.POST.get("message"))

    return render(request, "message/mycontacts.html", {"contacts": contacts})
