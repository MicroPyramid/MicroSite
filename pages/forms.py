from django import forms
from pages.models import Page, Menu

class PageForm(forms.ModelForm):

	class Meta:
		model = Page
		exclude = ('slug',)


class MenuForm(forms.ModelForm):

	class Meta:
		model = Menu
		exclude = ('lvl',)
