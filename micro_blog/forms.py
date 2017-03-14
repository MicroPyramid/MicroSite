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
    parent = forms.CharField(max_length=500, required=False)
    country = forms.CharField(max_length=500, required=False)

    def __init__(self, *args, **kwargs):
        # self.parent = kwargs.pop('parent', None)
        super(customPageCountryInlineFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        super(customPageCountryInlineFormSet, self).clean()

        if any(self.errors):
            return

        active_slugs = 0
        for form in self.forms:
            if form.cleaned_data.get("is_default"):
                active_slugs += 1

        if active_slugs > 1:
            print ("error form")
            raise forms.ValidationError(
                "Only one country data can be default at a time.")

    # def save_new(self, form, commit=True):
    #     print ("hello")
    #     instance = form.save(commit=False)
    #     print ("save new")
    #     print (instance)
    #     instance.parent = self.parent
    #     if commit:
    #         instance.save()
    #     return instance

    # def save_existing(self, form, instance, commit=True):
    #     print ("hello")
    #     return self.save_new(form, commit)

    # def save(self, commit=True):
    #     """
    #     Save model instances for every form, adding and changing instances
    #     as necessary, and return the list of instances.
    #     """
    #     if not commit:
    #         self.saved_forms = []

    #         def save_m2m():
    #             for form in self.saved_forms:
    #                 form.save_m2m()
    #         self.save_m2m = save_m2m
    #     return self.save_existing_objects(commit) + self.save_new_objects(commit)
