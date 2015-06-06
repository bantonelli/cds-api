# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kitbuilder.kitbuilder_v1.models
import amazon_file_field


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0012_auto_20150526_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitbuilderpurchase',
            name='zip_file',
            field=amazon_file_field.S3EnabledFileField(null=True, upload_to=kitbuilder.kitbuilder_v1.models.upload_kitbuilder_purchase_zip, blank=True),
        ),
    ]
