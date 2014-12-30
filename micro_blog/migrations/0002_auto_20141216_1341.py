# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('micro_blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcomments',
            name='phonenumber',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogcomments',
            name='weburl',
            field=models.CharField(default=datetime.date(2014, 12, 16), max_length=50),
            preserve_default=False,
        ),
    ]
