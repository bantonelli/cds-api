# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_userprofile_image'),
        ('kitbuilder_v1', '0006_auto_20150522_0627'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateFollow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_followed', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='follower',
            name='template',
        ),
        migrations.RemoveField(
            model_name='follower',
            name='user',
        ),
        migrations.AlterField(
            model_name='kitbuildertemplate',
            name='users_following',
            field=models.ManyToManyField(related_name='templates_followed', through='kitbuilder_v1.TemplateFollow', to='userprofile.UserProfile', blank=True),
        ),
        migrations.DeleteModel(
            name='Follower',
        ),
        migrations.AddField(
            model_name='templatefollow',
            name='template',
            field=models.ForeignKey(to='kitbuilder_v1.KitBuilderTemplate'),
        ),
        migrations.AddField(
            model_name='templatefollow',
            name='user',
            field=models.ForeignKey(to='userprofile.UserProfile'),
        ),
    ]
