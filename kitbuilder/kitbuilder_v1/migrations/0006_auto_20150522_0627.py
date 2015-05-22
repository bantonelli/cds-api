# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kitbuilder.kitbuilder_v1.models
import amazon_file_field


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0005_auto_20150522_0135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitbuildertemplate',
            name='image',
            field=amazon_file_field.S3EnabledImageField(upload_to=kitbuilder.kitbuilder_v1.models.upload_template_image, blank=True),
        ),
    ]
