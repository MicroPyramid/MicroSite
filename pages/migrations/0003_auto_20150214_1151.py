# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20150214_0834'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='doamin_url',
            new_name='domain_url',
        ),
        migrations.AlterField(
            model_name='contact',
            name='enquery_type',
            field=models.CharField(max_length=100, choices=[(b'general', b'Request For Services'), (b'partnership', b'Partnership Queries'), (b'media', b'Media Queries'), (b'general queries', b'General Queries'), (b'feedback', b'Website Feedback'), (b'others', b'Others')]),
            preserve_default=True,
        ),
    ]
