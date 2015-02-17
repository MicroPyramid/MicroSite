# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_leaves_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaves',
            name='date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
