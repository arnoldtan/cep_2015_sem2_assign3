# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoshare', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='followers',
        ),
        migrations.AddField(
            model_name='follower',
            name='followed',
            field=models.ForeignKey(related_name='followers', to='photoshare.UserProfile'),
        ),
        migrations.AddField(
            model_name='follower',
            name='follower',
            field=models.ForeignKey(related_name='following', to='photoshare.UserProfile'),
        ),
    ]
