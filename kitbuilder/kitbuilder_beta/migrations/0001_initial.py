# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kitbuilder.kitbuilder_beta.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_remove_userprofile_stuff'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomKit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('zip_file', models.FilePathField(max_length=200, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('on_sale', models.BooleanField(default=False)),
                ('soundcloud', models.CharField(max_length=500)),
                ('image', models.FileField(storage=kitbuilder.kitbuilder_beta.models.OverwriteStorage(), upload_to=kitbuilder.kitbuilder_beta.models.upload_kit_image)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KitDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('selling_point1', models.TextField(blank=True)),
                ('selling_point2', models.TextField(blank=True)),
                ('selling_point3', models.TextField(blank=True)),
                ('selling_point1_title', models.CharField(max_length=50, blank=True)),
                ('selling_point2_title', models.CharField(max_length=50, blank=True)),
                ('selling_point3_title', models.CharField(max_length=50, blank=True)),
                ('number_of_samples', models.IntegerField(default=0)),
                ('author', models.CharField(max_length=50, blank=True)),
                ('date_created', models.DateField(default=datetime.date(2015, 4, 21))),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('cost', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('percent_off', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('demo', models.FileField(storage=kitbuilder.kitbuilder_beta.models.OverwriteStorage(), upload_to=kitbuilder.kitbuilder_beta.models.upload_sample_demo)),
                ('wav', models.FileField(storage=kitbuilder.kitbuilder_beta.models.OverwriteStorage(), upload_to=kitbuilder.kitbuilder_beta.models.upload_sample)),
                ('type', models.CharField(max_length=2, choices=[(b'KD', b'Kick'), (b'SD', b'Snare'), (b'CP', b'Clap'), (b'PC', b'Percussion'), (b'FX', b'Sound FX'), (b'LO', b'Loop')])),
                ('kit', models.ForeignKey(related_name='samples', to='kitbuilder_beta.Kit')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='kit',
            name='description',
            field=models.ForeignKey(to='kitbuilder_beta.KitDescription'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kit',
            name='price',
            field=models.ForeignKey(to='kitbuilder_beta.Price'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kit',
            name='sale',
            field=models.ForeignKey(to='kitbuilder_beta.Sale'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kit',
            name='tags',
            field=models.ManyToManyField(to='kitbuilder_beta.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customkit',
            name='samples',
            field=models.ManyToManyField(to='kitbuilder_beta.Sample', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customkit',
            name='tags',
            field=models.ManyToManyField(to='kitbuilder_beta.Tag', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customkit',
            name='user',
            field=models.ForeignKey(related_name='custom_kits', to='userprofile.UserProfile'),
            preserve_default=True,
        ),
    ]
