# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dailyreport_files',
            name='dailyreport',
            field=models.ForeignKey(to='employee.DailyReport'),
        ),
        migrations.AddField(
            model_name='dailyreport',
            name='employee',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
