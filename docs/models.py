from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist


STATUS_CHOICES = (
        ('Approved','Approved'),
        ('Waiting','Waiting'),
        ('Rejected','Rejected'),
    )

PRIVACY_CHOICES = (
        ('Private', 'Private'),
        ('Public', 'Public'),
    )

class Book(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='books')
    title = models.CharField(max_length=100, unique = True)
    slug = models.SlugField(unique = True)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    updated_on = models.DateTimeField(auto_now_add=True)
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True)

    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES)

    def __unicode__(self):
        return self.title

    def create_book_slug(self, title_slug):
        slugcount = 0
        while True:
            
            try:
                Book.objects.get(slug = title_slug)
                slugcount = slugcount + 1
                title_slug = title_slug + '-' + str(slugcount)
            
            except ObjectDoesNotExist:
                return title_slug

    def save(self, *args, **kwargs):
        title_slug = slugify(self.title)
        
        if self.id:
            book = Book.objects.get(pk=self.id)
            
            if book.title != self.title:
                self.slug = self.create_book_slug(title_slug)
        else:
            self.slug = self.create_book_slug(title_slug)

        super(Book, self).save(*args, **kwargs)

    @property
    def owner(self):
        return self.admin.first_name + ' ' + self.admin.last_name


class Topic(models.Model):
    book = models.ForeignKey(Book)
    parent = models.ForeignKey('self', null=True, blank=True)

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique = True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    content = models.TextField()
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL)
    updated_on = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True)

    shadow = models.ForeignKey('self', null=True, blank=True, related_name='versions')

    def __unicode__(self):
        return self.title

    def create_topic_slug(self, title_slug):
        slugcount = 0
        while True:
            
            try:
                Topic.objects.get(slug = title_slug)
                slugcount = slugcount + 1
                title_slug = title_slug + '-' + str(slugcount)
            
            except ObjectDoesNotExist:
                return title_slug

    def save(self, *args, **kwargs):
        title_slug = slugify(self.title)
        
        if self.id:
            topic = Topic.objects.get(pk=self.id)
            
            if topic.title != self.title:
                self.slug = self.create_topic_slug(title_slug)
        else:
            self.slug = self.create_topic_slug(title_slug)

        super(Topic, self).save(*args, **kwargs)


class History(models.Model):
    topic = models.ForeignKey(Topic)

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique = True)

    date = models.DateTimeField(auto_now_add=True)
    
    content = models.TextField()
    
    def __unicode__(self):
        return self.title

    def create_slug(self, title_slug):
        slugcount = 0
        while True:
            
            try:
                History.objects.get(slug = title_slug)
                slugcount = slugcount + 1
                title_slug = title_slug + '-' + str(slugcount)
            
            except ObjectDoesNotExist:
                return title_slug
