from django import forms
from .models import Tweet

class TwitForm(forms.ModelForm):
    class Meta:
        model= Tweet
        fields=['text','photo']