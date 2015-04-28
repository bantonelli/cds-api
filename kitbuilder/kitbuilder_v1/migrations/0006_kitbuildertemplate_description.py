# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0005_auto_20150428_0529'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitbuildertemplate',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
