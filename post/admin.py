from django.contrib import admin
from .models import Post, Comment,ProfilePhoto, FriendRequest

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ProfilePhoto)
admin.site.register(FriendRequest)
