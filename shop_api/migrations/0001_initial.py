# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShopOrders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shop_name', models.CharField(max_length=200)),
                ('user_name', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('product_id', models.CharField(max_length=200)),
                ('task_status', models.CharField(max_length=1, choices=[(b'P', b'Pending'), (b'F', b'Failed'), (b'D', b'Done')])),
                ('task_id', models.CharField(max_length=50)),
            ],
        ),
    ]
