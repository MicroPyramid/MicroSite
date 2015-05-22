# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, max_length=10, choices=[(b'Approved', b'Approved'), (b'Waiting', b'Waiting'), (b'Rejected', b'Rejected')])),
                ('privacy', models.CharField(max_length=10, choices=[(b'Private', b'Private'), (b'Public', b'Public')])),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, max_length=10, choices=[(b'Approved', b'Approved'), (b'Waiting', b'Waiting'), (b'Rejected', b'Rejected')])),
            ],
        ),
    ]
