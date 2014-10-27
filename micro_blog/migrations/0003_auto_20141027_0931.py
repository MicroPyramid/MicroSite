# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('micro_blog', '0002_auto_20141018_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcomments',
            name='website',
        ),
        migrations.AlterField(
            model_name='blogcomments',
            name='email',
            field=models.EmailField(max_length=255),
        ),
    ]
