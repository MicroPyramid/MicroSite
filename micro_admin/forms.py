from django import forms
from micro_admin.models import User, career


class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField()
    newpassword = forms.CharField()
    retypepassword = forms.CharField()


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = [
                'username',
                'date_joined',
                'gender',
                'website',
                'last_login',
                'area',
                'fb_profile',
                'tw_profile',
                'ln_profile',
                'google_plus_url',
                "max_published_blogs",
                "min_published_blogs",
            ]


class CareerForm(forms.ModelForm):

    class Meta:
        model = career
        exclude = ['featured_image', 'slug', 'created_on']
