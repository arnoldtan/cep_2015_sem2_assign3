# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoshare', '0005_auto_20150817_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follower',
            name='accepted',
            field=models.BooleanField(default=None),
        ),
    ]
