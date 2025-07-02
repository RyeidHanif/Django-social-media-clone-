from django.urls import path
from . import views

urlpatterns = [
    path("msg/<int:reciever_id>/", views.chat_with, name="chat_with"),
]
