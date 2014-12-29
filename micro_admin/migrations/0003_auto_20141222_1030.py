# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('micro_admin', '0002_auto_20141219_0732'),
    ]

    operations = [
        migrations.RenameField(
            model_name='career',
            old_name='img_field',
            new_name='featured_image',
        ),
    ]
