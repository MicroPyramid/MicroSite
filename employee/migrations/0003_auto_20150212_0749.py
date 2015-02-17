# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_auto_20150212_0725'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dailyreport_files',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachments', models.FileField(upload_to=b'static/dailyreports/')),
                ('dailyreport', models.ForeignKey(to='employee.DailyReport')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='dailyreport',
            name='created_on',
            field=models.DateField(auto_now_add=True, unique=True),
            preserve_default=True,
        ),
    ]
