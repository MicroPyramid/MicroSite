from django import forms
from pages.models import Page, Menu, Contact
from micro_blog.models import Subscribers, Category


class PageForm(forms.ModelForm):
    # parent = forms.CharField(required=False)
    country = forms.CharField(required=False)

    class Meta:
        model = Page
        exclude = ('category',)

    def save(self, commit=True):
        instance = super(PageForm, self).save(commit=False)
        instance.country_id = self.cleaned_data['country']
        if commit:
            instance.save()
        return instance


class PageNewForm(forms.ModelForm):
    content = forms.CharField(required=False)
    # parent = forms.CharField(required=False)

    class Meta:
        model = Page
        exclude = ('category',)


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        exclude = ('lvl', 'url')


class ContactForm(forms.ModelForm):
    email = forms.EmailField()
    full_name = forms.CharField(max_length=200)
    message = forms.CharField(max_length=200)
    country = forms.CharField(max_length=200, required=False)
    enquery_type = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Contact
        exclude = ('full_name', 'message', 'email', 'phone', 'contact_info', 'country', 'enquery_type')

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        if 'country' in self.data.keys():
            self.fields['country'].required = True

        if 'enquery_type' in self.data.keys():
            self.fields['enquery_type'].required = True


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
