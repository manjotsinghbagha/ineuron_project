import code
from statistics import mode
from django.db import models
from django.contrib.auth.models import User

class MyCode(models.Model):
    code_name = models.CharField(max_length=100)
    code = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=20)
    def __str__(self):
        return self.code_name
