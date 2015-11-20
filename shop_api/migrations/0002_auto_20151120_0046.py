# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoporders',
            name='id',
        ),
        migrations.AddField(
            model_name='shoporders',
            name='quantity',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shoporders',
            name='task_id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
