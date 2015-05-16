# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_remove_userprofile_stuff'),
        ('kitbuilder_v1', '0002_remove_sample_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_followed', models.DateField(auto_now_add=True)),
                ('template', models.ForeignKey(to='kitbuilder_v1.KitBuilderTemplate')),
                ('user', models.ForeignKey(to='userprofile.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='kitbuildertemplate',
            name='followers',
            field=models.ManyToManyField(related_name='templates_followed', through='kitbuilder_v1.Follower', to='userprofile.UserProfile', blank=True),
        ),
    ]
