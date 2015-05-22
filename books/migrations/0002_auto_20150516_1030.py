# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='authors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='topic',
            name='book',
            field=models.ForeignKey(to='books.Book'),
        ),
        migrations.AddField(
            model_name='topic',
            name='parent',
            field=models.ForeignKey(blank=True, to='books.Topic', null=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='shadow',
            field=models.ForeignKey(related_name='versions', blank=True, to='books.Topic', null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='topic',
            field=models.ForeignKey(to='books.Topic'),
        ),
        migrations.AddField(
            model_name='book',
            name='admin',
            field=models.ForeignKey(related_name='books', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
