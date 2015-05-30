# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('micro_blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_display',
            field=models.BooleanField(default=False),
        ),
    ]
