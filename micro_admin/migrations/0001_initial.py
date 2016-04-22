# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=30)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address', db_index=True)),
                ('user_roles', models.CharField(max_length=10, choices=[('Admin', 'Admin'), ('PM', 'Project Manager'), ('Designer', 'Designer'), ('Developer', 'Developer')])),
                ('date_of_birth', models.DateField(default='1970-01-01')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_special', models.BooleanField(default=False)),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('gender', models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])),
                ('fb_profile', models.URLField(default='')),
                ('tw_profile', models.URLField(default='')),
                ('ln_profile', models.URLField(default='')),
                ('google_plus_url', models.URLField(default='')),
                ('about', models.CharField(default='', max_length=2000, null=True, blank=True)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('area', models.CharField(max_length=150)),
                ('address', models.TextField(default='', max_length=1000)),
                ('mobile', models.BigIntegerField(default='0')),
                ('website', models.URLField(default='', null=True)),
                ('phones', models.TextField(default='', max_length=100, null=True)),
                ('pincode', models.TextField(default='', max_length=50, null=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'permissions': (('blog_moderator', 'Can enable or disable blog posts'), ('blogger', 'Can write blog posts')),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='career',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('experience', models.CharField(max_length=100)),
                ('skills', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('featured_image', models.CharField(max_length=100, null=True, blank=True)),
                ('num_of_opening', models.IntegerField(default=True)),
                ('posted_on', models.DateField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('url', models.URLField(default='')),
            ],
        ),
    ]
