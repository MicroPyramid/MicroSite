from django import forms
from micro_blog.models import Post, Category


class BlogpostForm(forms.ModelForm):
    meta_description = forms.CharField(max_length=500, required=False)
    slug = forms.CharField(max_length=500, required=False)

    class Meta:
        model = Post
        exclude = ('tags', 'user', 'meta_description', 'published_on')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', "")
        super(BlogpostForm, self).__init__(*args, **kwargs)
        if self.data['is_superuser'] == 'True':
            self.fields['slug'].required = True


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)
