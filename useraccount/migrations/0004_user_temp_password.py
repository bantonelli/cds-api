# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0003_remove_user_testfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='temp_password',
            field=models.CharField(max_length=128, null=True, verbose_name='temp_password', blank=True),
            preserve_default=True,
        ),
    ]
