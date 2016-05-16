from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from micro_blog.models import Category


class Page(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    meta_title = models.TextField()
    meta_description = models.TextField()
    keywords = models.TextField()
    category = models.ManyToManyField(Category)

    # def save(self, *args, **kwargs):
    #     tempslug = slugify(self.title)
    #     if self.id:
    #         existed_page = Page.objects.get(pk=self.id)
    #         if existed_page.title != self.title:
    #             self.slug = create_slug(tempslug)
    #     else:
    #         self.slug = create_slug(tempslug)

    #     super(Page, self).save(*args, **kwargs)

    def all_categories(self):
        categories = Category.objects.all()
        if self.category.all().count() == categories.count():
            return True
        else:
            return False

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


def create_slug(tempslug):
    slugcount = 0
    while True:
        try:
            Page.objects.get(slug=tempslug)
            slugcount = slugcount + 1
            tempslug = tempslug + '-' + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug
