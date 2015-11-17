from django import forms
from micro_blog.models import Post, Category


class BlogpostForm(forms.ModelForm):
    meta_description = forms.CharField(max_length=500, required=False)

    class Meta:
        model = Post
        exclude = ('slug', 'tags', 'user', 'meta_description',)


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)
