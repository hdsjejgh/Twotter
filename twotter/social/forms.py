from django import forms
from .models import Twoot

class TwootForm(forms.ModelForm): #form for making twoots
    body = forms.CharField(required=True, widget = forms.widgets.Textarea(
        attrs={"placeholder":"Enter your Twoot", "class":"form-control"}), #form control class is for bootstrap to work
        label="")
    class Meta:
        model=Twoot #forms makes twoots
        exclude=("user",) #so you dont have to input user for making twoot