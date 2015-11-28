# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0004_auto_20151128_0048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoporders',
            old_name='key',
            new_name='key_memcached',
        ),
    ]
