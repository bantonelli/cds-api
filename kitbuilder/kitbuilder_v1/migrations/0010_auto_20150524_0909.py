# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0009_vendorkit_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='type',
            field=models.CharField(max_length=20, choices=[(b'Kick', b'Kick'), (b'Snare', b'Snare'), (b'Clap', b'Clap'), (b'Overhead', b'Overhead'), (b'Percussion', b'Percussion'), (b'Sound FX', b'Effect'), (b'Loop', b'Loop')]),
        ),
    ]
