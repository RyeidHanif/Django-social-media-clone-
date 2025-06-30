from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Messages(models.Model):
    content = models.CharField(max_length=100)
    sender = models.ForeignKey(
        User, related_name="messages_sent", on_delete=models.CASCADE
    )
    reciever = models.ForeignKey(
        User, related_name="messages_recieved", on_delete=models.CASCADE
    )
    timesent = models.DateTimeField(auto_now_add=True)
