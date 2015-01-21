# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('micro_admin', '0006_remove_career_applicant_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='career',
            name='url',
            field=models.URLField(default=b''),
            preserve_default=True,
        ),
    ]
