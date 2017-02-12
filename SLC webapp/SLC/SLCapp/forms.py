from django import forms
from django.contrib.auth.models import User
from SLCapp.models import UserProfile, SignUpPicture, ChatBotResponse

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('DoB', 'NationalInsuranceNo', 'PassportNo',)

class SignUpPictureForm(forms.ModelForm):
    class Meta:
        model = SignUpPicture
        fields = ('picture',)


class ChatBotResponseForm(forms.ModelForm):
    class Meta:
        model = ChatBotResponse
        fields = ('request', 'response', 'user',)



