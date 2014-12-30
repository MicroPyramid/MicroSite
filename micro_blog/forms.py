from django import forms
from micro_blog.models import Post, Category, BlogComments


class BlogpostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('slug','tags','user',)

class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComments
        exclude = ('status','post',)