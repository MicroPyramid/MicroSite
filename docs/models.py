from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify


STATUS_CHOICES = (
        ('Approved','Approved'),
        ('Waiting','Waiting'),
        ('Rejected','Rejected'),
    )

class Book(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='books')
    display_title = models.CharField(max_length=100)
    title = models.CharField(max_length=100, unique = True)
    slug = models.CharField(max_length=50, unique = True)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=2000)
    updated_on = models.DateTimeField(auto_now_add=True)
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True)

    def __unicode__(self):
        return self.display_title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

    @property
    def owner(self):
        return self.admin.first_name + ' ' + self.admin.last_name


class Topic(models.Model):
    book = models.ForeignKey(Book)
    parent = models.ForeignKey('self', null=True, blank=True)

    display_title = models.CharField(max_length=100)
    title = models.CharField(max_length=100, unique = True)
    slug = models.CharField(max_length=50, unique = True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    content = models.CharField(max_length=2000)
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL)
    updated_on = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True)

    shadow = models.ForeignKey('self', null=True, blank=True, related_name='versions')

    def __unicode__(self):
        return self.display_title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Topic, self).save(*args, **kwargs)

