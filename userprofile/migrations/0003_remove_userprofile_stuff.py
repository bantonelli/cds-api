# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_userprofile_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='stuff',
        ),
    ]
