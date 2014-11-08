from django import forms
from .models import User

class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField()
    newpassword = forms.CharField()
    retypepassword = forms.CharField()

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email','password','user_roles',)