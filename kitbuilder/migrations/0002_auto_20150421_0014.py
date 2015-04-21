# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customkit',
            name='samples',
        ),
        migrations.RemoveField(
            model_name='customkit',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='customkit',
            name='user',
        ),
        migrations.DeleteModel(
            name='CustomKit',
        ),
        migrations.RemoveField(
            model_name='kit',
            name='description',
        ),
        migrations.RemoveField(
            model_name='kit',
            name='price',
        ),
        migrations.RemoveField(
            model_name='kit',
            name='sale',
        ),
        migrations.RemoveField(
            model_name='kit',
            name='tags',
        ),
        migrations.DeleteModel(
            name='KitDescription',
        ),
        migrations.DeleteModel(
            name='Price',
        ),
        migrations.DeleteModel(
            name='Sale',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='kit',
        ),
        migrations.DeleteModel(
            name='Kit',
        ),
        migrations.DeleteModel(
            name='Sample',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
