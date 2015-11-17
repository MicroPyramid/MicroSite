# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('micro_blog', '0002_category_is_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='meta_description',
            field=models.TextField(default=b'', max_length=500),
        ),
    ]
