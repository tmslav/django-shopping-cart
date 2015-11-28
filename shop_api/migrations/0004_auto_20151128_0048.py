# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0003_auto_20151126_0035'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemcachedKeys',
            fields=[
                ('key', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('last_user', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='shoporders',
            name='key',
            field=models.ForeignKey(default=datetime.datetime(2015, 11, 28, 0, 48, 32, 362594, tzinfo=utc), to='shop_api.MemcachedKeys'),
            preserve_default=False,
        ),
    ]
