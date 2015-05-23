# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitbuilder_v1', '0007_auto_20150523_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatefollow',
            name='template',
            field=models.ForeignKey(related_name='follows', to='kitbuilder_v1.KitBuilderTemplate'),
        ),
        migrations.AlterField(
            model_name='templatefollow',
            name='user',
            field=models.ForeignKey(related_name='template_follows', to='userprofile.UserProfile'),
        ),
    ]
