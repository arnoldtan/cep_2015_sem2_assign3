# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoshare', '0003_auto_20150816_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(max_length=1000, upload_to=b'/Users/ata/Documents/ata/school/ri/academic/cep/year_three/web dev/Assignment3/assign3/photoshare/uploads/photos'),
        ),
    ]
