# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0003_auto_20150421_2340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kitbuildertemplate',
            old_name='times_sampled',
            new_name='times_added',
        ),
    ]
