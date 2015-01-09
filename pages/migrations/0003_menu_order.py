# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_simplecontact'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
