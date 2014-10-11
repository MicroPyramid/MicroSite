from django import forms

class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField()
    newpassword = forms.CharField()
    retypepassword = forms.CharField()