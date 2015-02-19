# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'email address', db_index=True)),
                ('user_roles', models.CharField(max_length=10, choices=[(b'Admin', b'Admin'), (b'PM', b'Project Manager'), (b'Designer', b'Designer'), (b'Developer', b'Developer')])),
                ('date_of_birth', models.DateField(default=b'1970-01-01')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('first_name', models.CharField(default=b'', max_length=100)),
                ('last_name', models.CharField(default=b'', max_length=100)),
                ('gender', models.CharField(max_length=10, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('fb_profile', models.URLField(default=b'')),
                ('tw_profile', models.URLField(default=b'')),
                ('ln_profile', models.URLField(default=b'')),
                ('google_plus_url', models.URLField(default=b'')),
                ('about', models.CharField(default=b'', max_length=2000, null=True, blank=True)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('area', models.CharField(max_length=150)),
                ('address', models.TextField(default=b'', max_length=1000)),
                ('mobile', models.BigIntegerField(default=b'0')),
                ('website', models.URLField(default=b'', null=True)),
                ('phones', models.TextField(default=b'', max_length=100, null=True)),
                ('pincode', models.TextField(default=b'', max_length=50, null=True)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_groups', verbose_name='groups', to='auth.Group', blank=True)),
                ('user_permissions', models.ManyToManyField(help_text=b'Specific permissions for this user.', related_name='user_permissions', verbose_name='user permissions', to='auth.Permission', blank=True)),
            ],
            options={
                'permissions': (('blog_moderator', 'Can enable or disable blog posts'), ('blogger', 'Can write blog posts')),
            },
            bases=(models.Model,),
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
                ('url', models.URLField(default=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
