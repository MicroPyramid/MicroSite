# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='website',
            new_name='doamin_url',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='company',
            new_name='domain',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='callback_time',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='contacted_on',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='content',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='email',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='name',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='timezone',
        ),
        migrations.AddField(
            model_name='contact',
            name='contact_info',
            field=models.ForeignKey(default=1, to='pages.simplecontact'),
            preserve_default=False,
        ),
    ]
