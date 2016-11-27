from django.contrib.auth.models import User
from django import forms

class userform(forms.ModelForm):
    password =forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields=['username','email','password']




