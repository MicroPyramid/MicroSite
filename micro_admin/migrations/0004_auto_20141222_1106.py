# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('micro_admin', '0003_auto_20141222_1030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='career',
            name='featured_image',
        ),
        migrations.AddField(
            model_name='career',
            name='img_field',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
