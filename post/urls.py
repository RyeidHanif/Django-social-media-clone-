from django.urls import path 
from . import views

urlpatterns=  [

    path('', views.home , name = "home"),

    path("addpost/", views.addpost , name = "addpost"),
    path("myposts/" , views.showmyposts , name = "showmyposts"),
    path("myfeed/" , views.showmyfeed , name = "showmyfeed"),
    path("mysettings/", views.mysettings , name = "mysettings"),
    path("modifypost/<int:postID>/", views.modifypost, name="modifypost"),
    path("showpostcomments/<int:postID>/", views.showcomments, name="showcomments"),
    path('dashboard/', views.dashboard , name = "dashboard")


]