# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_auto_20150213_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreport',
            name='created_on',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
