# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='category',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='requirements',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='skype',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='technology',
        ),
        migrations.AlterField(
            model_name='contact',
            name='domain',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='domain_url',
            field=models.URLField(null=True, blank=True),
        ),
    ]
