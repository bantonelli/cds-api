# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_beta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customkit',
            name='samples',
            field=models.ManyToManyField(to='kitbuilder_beta.Sample', blank=True),
        ),
        migrations.AlterField(
            model_name='customkit',
            name='tags',
            field=models.ManyToManyField(to='kitbuilder_beta.Tag', blank=True),
        ),
        migrations.AlterField(
            model_name='kitdescription',
            name='date_created',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
