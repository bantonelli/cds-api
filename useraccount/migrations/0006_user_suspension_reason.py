# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0005_user_suspended'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='suspension_reason',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
