# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0006_user_suspension_reason'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='suspended',
            new_name='is_suspended',
        ),
    ]
