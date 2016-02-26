from django import forms
from micro_blog.models import Post, Category
from django.db.models import Q


class BlogpostForm(forms.ModelForm):
    meta_description = forms.CharField(max_length=500, required=False)
    slug = forms.CharField(max_length=500, required=False)

    class Meta:
        model = Post
        exclude = ('tags', 'user', 'meta_description', 'published_on', 'old_slugs')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', "")
        super(BlogpostForm, self).__init__(*args, **kwargs)
        if self.data['is_superuser'] == 'True':
            self.fields['slug'].required = True

    def clean_slug(self):
        if self.data['is_superuser'] == 'True':
            blog_posts = Post.objects.filter(Q(slug=self.data.get('slug')) | Q(old_slugs__icontains=self.data.get('slug'))).exclude(id=self.instance.id)
            if blog_posts:
                raise forms.ValidationError('Blog Post with this slug already exists')
            else:
                return self.data['slug']


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)
