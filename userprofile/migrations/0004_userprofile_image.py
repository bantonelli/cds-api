# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import userprofile.models
import amazon_file_field


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_remove_userprofile_stuff'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=amazon_file_field.S3EnabledImageField(upload_to=userprofile.models.upload_profile_image, blank=True),
        ),
    ]
