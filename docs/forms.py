from django import forms
from docs.models import Book, Topic


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('slug','authors')


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ('slug','authors')
