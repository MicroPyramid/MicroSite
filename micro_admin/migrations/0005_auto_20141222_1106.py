# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('micro_admin', '0004_auto_20141222_1106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='career',
            old_name='img_field',
            new_name='featured_image',
        ),
    ]
