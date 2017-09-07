from django import forms
from micro_blog.models import Post, Category


class BlogpostForm(forms.ModelForm):
    meta_description = forms.CharField(max_length=500, required=False)

    class Meta:
        model = Post
        exclude = ('tags', 'user', 'published_on', 'old_slugs')


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)


class CustomBlogSlugInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(CustomBlogSlugInlineFormSet, self).clean()
        if any(self.errors):
            return
        active_slugs = 0
        for form in self.forms:
            if form.cleaned_data.get("is_active"):
                active_slugs += 1
        if active_slugs > 1:
            raise forms.ValidationError(
                "Only one slug can be active at a time.")


class PlagiarismForm(forms.Form):
    description = forms.CharField(max_length=50000)