from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from phonenumber_field .formfields import PhoneNumberField
from django import forms
from .models import Product, Chat

User = get_user_model()

class RegisterForm(UserCreationForm):

    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    phonenumber = forms.CharField(max_length=15)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'phonenumber', 'first_name','last_name','email','password1', 'password2' )
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username Already Exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email Already Exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.save()
        return user

