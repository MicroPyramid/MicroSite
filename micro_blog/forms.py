from django import forms
from micro_blog.models import Post, Category
from django.db.models import Q


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


class customPageCountryInlineFormSet(forms.BaseModelFormSet):
    content = forms.CharField(max_length=500, required=False)
    parent = forms.CharField(max_length=500, required=False)

    def clean(self):
        super(customPageCountryInlineFormSet, self).clean()
        print (self.errors)
        if any(self.errors):
            return
        # default_countries = 0
        # for form in self.forms:
        #     if form.cleaned_data.get("is_default"):
        #         default_countries += 1
        # if default_countries > 1:
        #     raise forms.ValidationError(
        #         "Only one slug can be active at a time.")
