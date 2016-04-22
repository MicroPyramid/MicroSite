from django import forms
from pages.models import Page, Menu, simplecontact, Contact
from micro_blog.models import Subscribers, Category


class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        exclude = ('category',)


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


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(SubscribeForm, self).__init__(*args, **kwargs)

    def clean_email(self):

        if str(self.data['is_blog']) == 'True':
            if len(self.data['is_category']) > 0:
                category = Category.objects.get(id=self.data['is_category'])
                existing_subscribers = Subscribers.objects.filter(email=self.data['email'], blog_post=True, category=category)
            else:
                existing_subscribers = Subscribers.objects.filter(email=self.data['email'], blog_post=True, category=None)
        else:
            existing_subscribers = Subscribers.objects.filter(email=self.data['email'], blog_post=False)
        if existing_subscribers:
            raise forms.ValidationError('User with email id is already Subscribed')

        return self.data['email']
