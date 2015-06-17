# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20150516_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='display_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='keywords',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='topic',
            name='display_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='topic',
            name='keywords',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
