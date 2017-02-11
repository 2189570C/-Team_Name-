from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    #gender = 
    DoB = models.DateField()
    NationalInsuranceNo = models.CharField(max_length=9)
    PassportNo = models.IntegerField(max_length=9)
    
    def __str__(self):
        return self.user.username
    
    def __unicode__(self):
        return self.user.username


class SignUpPicture(models.Model):
    picture = models.ImageField()
