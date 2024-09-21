from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True)

    def __str__(self):
        return  self.username


class Question(models.Model):
    questionid= models.CharField(max_length=100,primary_key=True)
    userid = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=20,blank=True, null=True)


    def __str__(self):
        return  self.title


class Answer(models.Model):
    answerid = models.AutoField(primary_key=True)
    questionid = models.ForeignKey('Question', on_delete=models.CASCADE)
    userid = models.ForeignKey('User', on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return self.answerid

