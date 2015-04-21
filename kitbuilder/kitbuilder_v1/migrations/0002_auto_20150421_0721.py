# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='bpm',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='duration',
            field=models.DurationField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='type',
            field=models.CharField(max_length=20, choices=[(b'Kick', b'Kick'), (b'Snare', b'Snare'), (b'Clap', b'Clap'), (b'Overhead', b'Overhead'), (b'Percussion', b'Percussion'), (b'Sound FX', b'Sound FX'), (b'Loop', b'Loop')]),
        ),
        migrations.AlterField(
            model_name='sample',
            name='vendor_kit',
            field=models.ForeignKey(related_name='samples', blank=True, to='kitbuilder_v1.VendorKit'),
        ),
    ]
