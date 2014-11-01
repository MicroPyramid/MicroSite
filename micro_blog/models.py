from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
import datetime

def create_slug(tempslug):
    slugcount = 0
    while True:
        try:
            Post.objects.get(slug = tempslug)
            slugcount = slugcount + 1
            tempslug = tempslug + '-' + str(slugcount)
        except:
            return tempslug
            break

class Category(models.Model):
    name = models.CharField(max_length=20, unique = True)
    slug = models.CharField(max_length=20, unique = True)
    description = models.CharField(max_length=500)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Tags(models.Model):
    name = models.CharField(max_length=20, unique = True)
    slug = models.CharField(max_length=20, unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tags, self).save(*args, **kwargs)

class Post(models.Model):
    STATUS_CHOICE = (
                    ('D','Draft'),
                    ('P','Published'),
                    ('T','Rejected'),
                    )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(max_length=10000)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tags,blank=True,null=True)
    featured_image = models.CharField(max_length=400, blank=True, null=True)
    featured_post = models.CharField(max_length=4, default='off',blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICE,blank=True)

    @property
    def author(self):
        return self.user.first_name + ' ' + self.user.last_name

    def save(self, *args, **kwargs):
        tempslug = slugify(self.title)
        if self.id:
            blogpost = Post.objects.get(pk=self.id)
            if blogpost.title != self.title:
                self.slug = create_slug(tempslug)
        else:
            self.slug = create_slug(tempslug)

        super(Post, self).save(*args, **kwargs)

class BlogComments(models.Model):
    post = models.ForeignKey(Post, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length=3,default="off", blank=True)

class Image_File(models.Model):
    upload = models.FileField(upload_to="static/uploads/%Y/%m/%d/")
    date_created = models.DateTimeField(default=datetime.datetime.now)
    is_image = models.BooleanField(default=True)
    thumbnail = models.FileField(upload_to="static/uploads/%Y/%m/%d/",blank=True,null=True)
