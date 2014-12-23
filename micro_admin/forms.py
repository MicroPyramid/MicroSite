from django import forms
from .models import User,career

class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField()
    newpassword = forms.CharField()
    retypepassword = forms.CharField()

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email','password','user_roles',)

class CareerForm(forms.ModelForm):

	class Meta:
		model = career
		exclude = ['featured_image','slug','applicant_name','created_on','is_active']
