# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=100, choices=[(b'Hire', b'Hire Us'), (b'Contact', b'Contact Us'), (b'Report', b'Report Issue')])),
                ('domain', models.CharField(max_length=100)),
                ('domain_url', models.URLField()),
                ('skype', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=100)),
                ('budget', models.IntegerField()),
                ('technology', models.CharField(max_length=100)),
                ('requirements', models.CharField(max_length=200, choices=[(b'new site', b'New website from scratch'), (b'revamp', b'Revamp existing website / application'), (b'new features', b'Addition of new features'), (b'minor changes', b'Minor design changes / tweaks'), (b'integration', b'Integrate selected platform into my website'), (b'security', b'Enhance security to my application'), (b'performance', b'Tune performance of my application'), (b'maintenance', b'Maintenance of web application / server'), (b'payment gateway', b'Integrate / enhance payment gateway')])),
                ('enquery_type', models.CharField(max_length=100, choices=[(b'general', b'Request For Services'), (b'partnership', b'Partnership Queries'), (b'media', b'Media Queries'), (b'general queries', b'General Queries'), (b'feedback', b'Website Feedback'), (b'others', b'Others')])),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default=b'off', max_length=5, blank=True)),
                ('lvl', models.IntegerField()),
                ('parent', models.ForeignKey(blank=True, to='pages.Menu', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('slug', models.SlugField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='simplecontact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.BigIntegerField(null=True, blank=True)),
                ('contacted_on', models.DateField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='contact',
            name='contact_info',
            field=models.ForeignKey(to='pages.simplecontact'),
        ),
    ]
