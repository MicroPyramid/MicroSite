# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('micro_admin', '0005_auto_20141222_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='career',
            name='applicant_name',
        ),
    ]
