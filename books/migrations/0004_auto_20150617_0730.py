# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20150617_0553'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['display_order']},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['display_order']},
        ),
    ]
