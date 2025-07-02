from django.urls import path 
from . import views

urlpatterns=  [

    path('', views.home , name = "home"),

    path("addpost/", views.addpost , name = "addpost"),
    path("myposts/" , views.showmyposts , name = "showmyposts"),
    path("myfeed/" , views.showmyfeed , name = "showmyfeed"),
    path("settings/", views.settings , name = "settings"),
    path("modifypost/<int:postID>/", views.modifypost, name="modifypost"),
    path("showcomments/<int:postID>/", views.showcomments, name="showcomments"),
    path('dashboard/', views.dashboard , name = "dashboard"),
    path('aboutuser/<int:user_id>', views.aboutuser, name="aboutuser"),
    path('friends/', views.friends ,name="friends"),
    path("viewrecom/", views.viewrecom, name="viewrecom"),
    path("viewpending/", views.viewpending , name = "viewpending"),
    path("whatsnew/" , views.whatsnew , name = "whatsnew")
]

