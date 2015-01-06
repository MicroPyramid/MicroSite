from django import forms
from micro_blog.models import Post


class BlogForm(forms.ModelForm):

	class Meta:
		model = Post
		exclude = ('tags','status','slug',)
