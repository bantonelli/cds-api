# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0002_auto_20150421_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='vendor_kit',
            field=models.ForeignKey(related_name='samples', blank=True, to='kitbuilder_v1.VendorKit', null=True),
        ),
    ]
