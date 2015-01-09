from django import forms
from pages.models import Page, Menu,simplecontact

class  PageForm(forms.ModelForm):

	class Meta:
		model = Page
		exclude = ('slug',)


class MenuForm(forms.ModelForm):

	class Meta:
		model = Menu
		exclude = ('lvl',)

class ContactForm(forms.ModelForm):
	class Meta:
		model=simplecontact
		fields=('full_name','message','email','phone')