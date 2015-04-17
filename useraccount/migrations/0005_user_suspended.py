# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0004_user_temp_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='suspended',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
