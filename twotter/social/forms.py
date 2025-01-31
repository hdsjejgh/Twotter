from django import forms
from .models import Twoot
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TwootForm(forms.ModelForm): #form for making twoots
    body = forms.CharField(required=True, widget = forms.widgets.Textarea(
        attrs={"placeholder":"Enter your Twoot", "class":"form-control"}), #form control class is for bootstrap to work
        label="")
    class Meta:
        model=Twoot #forms makes twoots
        exclude=("user",) #so you dont have to input user for making twoot



class RegisterForm(UserCreationForm): #form for registering user
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={"placeholder":"Email", "class":"form-control"}))
    username = forms.CharField(max_length=32, label="", widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}))

    class Meta:
        model = User
        fields = ("username","email","password1","password2") #fields to add to newly made user

    def __init__(self, *args, **kwargs): #django users have username and password already built in, so this stuff fixes that, dont really know what it does i just copied it
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

