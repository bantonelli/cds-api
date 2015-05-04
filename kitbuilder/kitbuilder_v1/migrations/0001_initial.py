# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
import kitbuilder.kitbuilder_v1.models
import amazon_file_field


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_remove_userprofile_stuff'),
    ]

    operations = [
        migrations.CreateModel(
            name='KitBuilderPurchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('date_purchased', models.DateField(auto_now_add=True)),
                ('zip_file', models.FilePathField(max_length=250, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='KitBuilderTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('last_updated', models.DateField(auto_now=True)),
                ('times_added', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True)),
                ('featured', models.BooleanField(default=False)),
                ('public', models.BooleanField(default=False)),
                ('image', amazon_file_field.S3EnabledImageField(upload_to=kitbuilder.kitbuilder_v1.models.upload_template_image)),
            ],
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
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=20, choices=[(b'Kick', b'Kick'), (b'Snare', b'Snare'), (b'Clap', b'Clap'), (b'Overhead', b'Overhead'), (b'Percussion', b'Percussion'), (b'Sound FX', b'Sound FX'), (b'Loop', b'Loop')])),
                ('bpm', models.IntegerField(default=0, null=True, blank=True)),
                ('duration', models.DurationField(null=True, blank=True)),
                ('key', models.CharField(max_length=10, null=True, blank=True)),
                ('preview', models.TextField()),
                ('wav', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(null=True, blank=True)),
                ('logo', amazon_file_field.S3EnabledImageField(upload_to=kitbuilder.kitbuilder_v1.models.upload_vendor_logo)),
                ('facebook', models.URLField(null=True, blank=True)),
                ('twitter', models.URLField(null=True, blank=True)),
                ('google_plus', models.URLField(null=True, blank=True)),
                ('soundcloud', models.URLField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VendorKit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('on_sale', models.BooleanField(default=False)),
                ('soundcloud', models.CharField(max_length=500)),
                ('image', amazon_file_field.S3EnabledImageField(upload_to=kitbuilder.kitbuilder_v1.models.upload_vendor_kit_image)),
                ('description', tinymce.models.HTMLField(blank=True)),
                ('sample_count', models.IntegerField(null=True, blank=True)),
                ('commission_rate', models.DecimalField(max_digits=10, decimal_places=2)),
                ('price', models.ForeignKey(to='kitbuilder_v1.Price')),
                ('sale', models.ForeignKey(to='kitbuilder_v1.Sale')),
                ('tags', models.ManyToManyField(to='kitbuilder_v1.Tag')),
                ('vendor', models.ForeignKey(to='kitbuilder_v1.Vendor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='sample',
            name='vendor_kit',
            field=models.ForeignKey(related_name='samples', to='kitbuilder_v1.VendorKit'),
        ),
        migrations.AddField(
            model_name='kitbuildertemplate',
            name='samples',
            field=models.ManyToManyField(to='kitbuilder_v1.Sample', blank=True),
        ),
        migrations.AddField(
            model_name='kitbuildertemplate',
            name='tags',
            field=models.ManyToManyField(to='kitbuilder_v1.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='kitbuildertemplate',
            name='user',
            field=models.ForeignKey(related_name='kitbuilder_templates', to='userprofile.UserProfile'),
        ),
        migrations.AddField(
            model_name='kitbuilderpurchase',
            name='samples',
            field=models.ManyToManyField(to='kitbuilder_v1.Sample', blank=True),
        ),
        migrations.AddField(
            model_name='kitbuilderpurchase',
            name='user',
            field=models.ForeignKey(related_name='kitbuilder_purchases', to='userprofile.UserProfile'),
        ),
    ]
