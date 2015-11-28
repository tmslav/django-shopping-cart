# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0002_auto_20151120_0046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoporders',
            old_name='password',
            new_name='client_ip',
        ),
        migrations.RemoveField(
            model_name='shoporders',
            name='user_name',
        ),
    ]
