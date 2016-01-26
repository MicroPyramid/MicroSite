from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from micro_blog.models import Post
from django.template.defaultfilters import slugify
from django.utils import timezone


GENDER_TYPES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

USER_ROLES = (
              ('Admin', 'Admin'),
              ('PM', 'Project Manager'),
              ('Designer', 'Designer'),
              ('Developer', 'Developer'),
              )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, db_index=True,)
    user_roles = models.CharField(choices=USER_ROLES, max_length=10)
    date_of_birth = models.DateField(default='1970-01-01')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_special = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    gender = models.CharField(choices=GENDER_TYPES, max_length=10)
    fb_profile = models.URLField(default='')
    tw_profile = models.URLField(default='')
    ln_profile = models.URLField(default='')
    google_plus_url = models.URLField(default='')
    about = models.CharField(max_length=2000, default='', null=True, blank=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=150)
    address = models.TextField(max_length=1000, default='')
    mobile = models.BigIntegerField(default='0')
    website = models.URLField(default='', null=True)
    phones = models.TextField(max_length=100, default='', null=True)
    pincode = models.TextField(max_length=50, default='', null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __unicode__(self):
        return self.first_name + ' (' + self.email + ')'

    def total_posts(self):
        return Post.objects.filter(user=self).count()

    def drafted_posts(self):
        return Post.objects.filter(user=self, status="D").count()

    class Meta:
        permissions = (
            ("blog_moderator", "Can enable or disable blog posts"),
            ("blogger", "Can write blog posts"),
        )


class career(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    experience = models.CharField(max_length=100)
    skills = models.CharField(max_length=100)
    description = models.TextField()
    featured_image = models.CharField(max_length=100, blank=True, null=True)
    num_of_opening = models.IntegerField(default=True)
    posted_on = models.DateField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    url = models.URLField(default='')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(career, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
