from django.db import models

# Create your models here.
class Post(models.Model):
    uname = models.CharField(max_length=130, default='admin')
    title = models.CharField(max_length=150)
    desc = models.TextField()

 