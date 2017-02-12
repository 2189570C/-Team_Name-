from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    #gender = 
    DoB = models.DateField()
    NationalInsuranceNo = models.CharField(max_length=9)
    PassportNo = models.CharField(max_length=9)
    
    def __str__(self):
        return self.user.username
    
    def __unicode__(self):
        return self.user.username


class SignUpPicture(models.Model):
    picture = models.ImageField()


class ChatBotResponse(models.Model):
    user = models.ForeignKey(User, blank=True)
    request = models.TextField()
    response = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.request

    def __unicode__(self):
        return self.user.request


class ChatBotContext(models.Model):
    user = models.ForeignKey(User)
    
    conversation_id = models.TextField()
    dialog_node = models.TextField()
    dialog_turn_counter = models.IntegerField()
    dialog_request_counter = models.IntegerField()
    defaultCounter = models.IntegerField(default=0)

    def __str__(self):
        return self.user.context

    def __unicode__(self):
        return self.user.context
