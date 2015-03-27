# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0002_user_testfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='testField',
        ),
    ]
