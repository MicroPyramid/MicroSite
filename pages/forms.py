from django import forms
from pages.models import *
class PageForm(forms.ModelForm):
	
	class Meta:
		model = page
		exclude = ('category', 'status','slug',)


class MenuForm(forms.ModelForm):
	
	class Meta:
		model = Menu
		exclude = ('url', 'created','target',)	
		