# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0003_auto_20150516_0601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kitbuildertemplate',
            name='times_added',
        ),
    ]
