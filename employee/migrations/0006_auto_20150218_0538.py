# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_auto_20150213_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyreport',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 2, 18, 5, 38, 35, 687066)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='leaves',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 18, 5, 38, 41, 699838), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dailyreport',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='leaves',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 2, 18, 5, 38, 55, 861679)),
            preserve_default=False,
        ),
    ]
