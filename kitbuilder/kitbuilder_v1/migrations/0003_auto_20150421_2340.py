# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kitbuilder.kitbuilder_v1.models


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0002_vendorkit_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kitbuildertemplate',
            old_name='purchases',
            new_name='times_sampled',
        ),
        migrations.AlterField(
            model_name='vendor',
            name='logo',
            field=models.FileField(storage=kitbuilder.kitbuilder_v1.models.OverwriteStorage(), upload_to=kitbuilder.kitbuilder_v1.models.upload_vendor_logo),
        ),
    ]
