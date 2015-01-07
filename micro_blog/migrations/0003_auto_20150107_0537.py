# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('micro_blog', '0002_auto_20141216_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='rel_posts', null=True, to='micro_blog.Tags', blank=True),
            preserve_default=True,
        ),
    ]
