import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from lxml import html


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    is_display = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @property
    def get_url(self):
        return settings.SITE_BLOG_URL + "category/" + self.slug

    def get_blog_posts(self):
        return Post.objects.filter(category=self, status='P')

    def no_of_blog_posts(self):
        return Post.objects.filter(category=self).count()


class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        tempslug = slugify(self.name)
        if self.id:
            tag = Tags.objects.get(pk=self.id)
            if tag.name != self.name:
                self.slug = create_tag_slug(tempslug)
        else:
            self.slug = create_tag_slug(tempslug)
        super(Tags, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


def create_tag_slug(tempslug):
    slugcount = 0
    while True:
        try:
            Tags.objects.get(slug=tempslug)
            slugcount = slugcount + 1
            tempslug = tempslug + '-' + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug


def get_blog_slug(slug):
    slugcount = 0
    tempslug = slug
    while True:
        try:
            Post_Slugs.objects.get(slug=tempslug)
            slugcount += 1
            tempslug = slug + '-' + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug


class Post(models.Model):
    STATUS_CHOICE = (
                    ('D', 'Draft'),
                    ('P', 'Published'),
                    ('T', 'Rejected'),
                    ('R', 'Review'),
                    )

    title = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    excerpt = models.CharField(max_length=500, default="")
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tags, related_name='rel_posts', blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICE, blank=True)
    published_on = models.DateField(blank=True, null=True)
    meta_description = models.TextField(max_length=500, default='')
    old_slugs = models.TextField()

    def __unicode__(self):
        return self.title

    def create_blog_slug(self, slugs):
        for each_slug in list(set(slugs)):
            blog_slugs = self.slugs.filter(slug=each_slug)
            if not blog_slugs:
                actual_slug = get_blog_slug(each_slug)
                Post_Slugs.objects.create(
                    blog=self, slug=actual_slug, is_active=False
                )

    def check_and_activate_slug(self):
        # Check whether active slug is their for blog-post or not
        blog_slugs = self.slugs.all().order_by("id")
        if not blog_slugs.filter(is_active=True):
            active_slug = blog_slugs.last()
            active_slug.is_active = True
            active_slug.save()

    @property
    def slug(self):
        blog_slug = self.slugs.filter(is_active=True).first()
        if blog_slug:
            return str(blog_slug.slug)
        return ""

    @property
    def author(self):
        return self.user.first_name + ' ' + self.user.last_name

    def save(self, *args, **kwargs):
        if self.status == 'P':
            if not self.published_on:
                self.published_on = datetime.datetime.today()
        super(Post, self).save(*args, **kwargs)

    @property
    def get_url(self):
        return settings.SITE_BLOG_URL + self.slug

    def is_editable_by(self, user):
        if self.user == user or user.is_superuser:
            return True
        return False

    def is_deletable_by(self, user):
        if self.user == user or user.is_superuser:
            return True
        return False

    def get_content(self):
        table = html.fromstring(self.content)
        content = ''
        for item in table:
            if item.text:
                content += item.text.strip()
        return content[:350]


class Post_Slugs(models.Model):
    blog = models.ForeignKey(Post, related_name='slugs')
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)


class Image_File(models.Model):
    upload = models.FileField(upload_to="static/uploads/%Y/%m/%d/")
    date_created = models.DateTimeField(default=datetime.datetime.now)
    is_image = models.BooleanField(default=True)
    thumbnail = models.FileField(upload_to="static/uploads/%Y/%m/%d/", blank=True, null=True)

    def __unicode__(self):
        return self.date_created


def create_slug(tempslug):
    slugcount = 0
    while True:
        try:
            Post.objects.get(slug=tempslug)
            slugcount = slugcount + 1
            tempslug = tempslug + '-' + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug


class Subscribers(models.Model):
    email = models.EmailField(max_length=255)
    created = models.DateField(auto_now_add=True)
    blog_post = models.BooleanField(default=True)
    category = models.ForeignKey(Category, blank=True, null=True)

    def __str__(self):
        return self.email
