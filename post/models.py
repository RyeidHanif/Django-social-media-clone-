from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    postname = models.CharField(max_length=50, unique=True)
    content = models.TextField(max_length=500)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    banner = models.ImageField(
        upload_to="media/", blank=True, null=True
    )  # image not compulsory , blanke = true so form can be mepty and null so db can add emtpy
    date_posted = models.DateTimeField(
        auto_now_add=True
    )  # user does not have to add the date, auto adds the current date
    owner = models.ForeignKey(
        User, related_name="posts_set", on_delete=models.CASCADE
    )  # foreign key to the User class


class Comment(models.Model):
    content = models.TextField(max_length=100)
    post = models.ForeignKey(
        Post, related_name="comments_set", on_delete=models.CASCADE
    )
    date_added = models.DateTimeField(auto_now_add=True)


class ProfilePhoto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)


# Create your models here.
