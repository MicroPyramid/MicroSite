from django import forms
from pages.models import Page, Menu, simplecontact, Contact


class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        exclude = ('slug',)


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        exclude = ('lvl',)


class SimpleContactForm(forms.ModelForm):
    class Meta:
        model = simplecontact
        fields = ('full_name', 'message', 'email', 'phone')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('full_name', 'message', 'email', 'phone', 'contact_info')
