from django.db import models
# Create your models here.

class GArequest(models.Model):
    size = models.IntegerField()
    board = models.CharField(max_length=200)

class GAresponse(models.Model):
    steps = models.CharField(max_length=200)