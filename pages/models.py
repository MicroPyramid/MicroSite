from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from micro_blog.models import Category, Country
from django.contrib.postgres.fields import ArrayField, JSONField
import json


class Page(models.Model):
    title = models.CharField(max_length=500)
    country = models.ForeignKey(Country, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    content = models.TextField()
    slug = models.SlugField()
    is_active = models.BooleanField(default=False)
    meta_data = models.TextField()
    category = models.ManyToManyField(Category)
    contact_info = JSONField(default={})

    # def save(self, *args, **kwargs):
    #     tempslug = slugify(self.title)
    #     if self.id:
    #         existed_page = Page.objects.get(pk=self.id)
    #         if existed_page.title != self.title:
    #             self.slug = create_slug(tempslug)
    #     else:
    #         self.slug = create_slug(tempslug)

    #     super(Page, self).save(*args, **kwargs)
    def get_contact_info(self):
        if self.contact_info:
            return json.dumps(self.contact_info)
        else:
            return ''

    def all_categories(self):
        categories = Category.objects.all()
        if self.category.all().count() == categories.count():
            return True
        else:
            return False

    def related_pages(self):
        menu = Menu.objects.filter(url=self.slug)
        menus = Menu.objects.filter(parent=menu[0].parent, status='on')
        return menus

    def __unicode__(self):
        return self.title


class Contact(models.Model):

    ENQUERY_TYPES = (
                    ('general', 'Request For Services'),
                    ('partnership', 'Partnership Queries'),
                    ('media', 'Media Queries'),
                    ('general queries', 'General Queries'),
                    ('feedback', 'Website Feedback'),
                    ('others', 'Others'),
                    )

    domain = models.CharField(max_length=100, null=True, blank=True)
    domain_url = models.URLField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=100)
    enquery_type = models.CharField(max_length=100, choices=ENQUERY_TYPES)

    # def __unicode__(self):
    #     return self.contact_info.full_name


class Menu(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    title = models.CharField(max_length=255)
    country = models.ForeignKey(Country, blank=True, null=True)
    url = models.URLField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=5, default="off", blank=True)
    lvl = models.IntegerField()

    def menu_state(self):
        if self.status == 'on':
            return True
        else:
            return False

    def __unicode__(self):
        return self.title

    def has_children(self):
        if self.menu_set.exists():
            return True
        return False

    def is_child(self):
        if self.parent:
            return True
        return False

    def get_active_children(self):
        return self.menu_set.filter(status='on').order_by('lvl')


def create_slug(tempslug):
    slugcount = 0
    while True:
        try:
            Page.objects.get(slug=tempslug)
            slugcount = slugcount + 1
            tempslug = tempslug + '-' + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug
