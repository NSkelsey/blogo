from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=120)
    body = models.CharField(max_length=5000)
    user = models.ForeignKey(User)
    date_last_edit = models.DateTimeField(auto_now=True)
    markup = models.BooleanField()
    quality = models.BooleanField()



class Vote(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
