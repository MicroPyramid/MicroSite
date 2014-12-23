# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('micro_admin', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='career',
            old_name='expirence',
            new_name='experience',
        ),
    ]
