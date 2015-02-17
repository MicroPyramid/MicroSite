# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150214_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplecontact',
            name='phone',
            field=models.BigIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
