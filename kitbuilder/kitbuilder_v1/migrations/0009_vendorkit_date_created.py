# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0008_auto_20150523_0412'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorkit',
            name='date_created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
