# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0004_remove_kitbuildertemplate_times_added'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kitbuildertemplate',
            old_name='followers',
            new_name='users_following',
        ),
    ]
