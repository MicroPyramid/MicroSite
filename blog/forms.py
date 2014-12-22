from django import forms
from blog.models import *



class BlogForm(forms.ModelForm):

	class Meta:
		model = Post
		exclude = ('tags','status','slug',)
