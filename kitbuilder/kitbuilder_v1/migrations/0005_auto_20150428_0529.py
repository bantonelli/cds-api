# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kitbuilder.kitbuilder_v1.models


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0004_auto_20150423_0436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitbuildertemplate',
            name='image',
            field=models.ImageField(storage=kitbuilder.kitbuilder_v1.models.OverwriteStorage(), null=True, upload_to=kitbuilder.kitbuilder_v1.models.upload_template_image, blank=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='logo',
            field=models.ImageField(storage=kitbuilder.kitbuilder_v1.models.OverwriteStorage(), upload_to=kitbuilder.kitbuilder_v1.models.upload_vendor_logo),
        ),
        migrations.AlterField(
            model_name='vendorkit',
            name='image',
            field=models.ImageField(storage=kitbuilder.kitbuilder_v1.models.OverwriteStorage(), upload_to=kitbuilder.kitbuilder_v1.models.upload_vendor_kit_image),
        ),
    ]
