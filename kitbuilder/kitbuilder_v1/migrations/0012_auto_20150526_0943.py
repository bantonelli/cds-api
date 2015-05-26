# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kitbuilder.kitbuilder_v1.models
import amazon_file_field


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0011_auto_20150524_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitbuildertemplate',
            name='image',
            field=amazon_file_field.S3EnabledImageField(null=True, upload_to=kitbuilder.kitbuilder_v1.models.upload_template_image, blank=True),
        ),
    ]
