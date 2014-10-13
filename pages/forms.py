from django import forms
from pages.models import page, Menu

class PageForm(forms.ModelForm):

	class Meta:
		model = page
		exclude = ('slug',)


class MenuForm(forms.ModelForm):
	
	class Meta:
		model = Menu
		exclude = ('lvl',)	
		