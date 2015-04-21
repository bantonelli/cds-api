# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorkit',
            name='description',
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]
