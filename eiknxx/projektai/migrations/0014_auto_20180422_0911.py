# Generated by Django 2.0 on 2018-04-22 06:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projektai', '0013_auto_20180422_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='old_projektas',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 22, 9, 11, 28, 771190)),
        ),
        migrations.AlterField(
            model_name='old_task',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 22, 9, 11, 28, 771190)),
        ),
        migrations.AlterField(
            model_name='syncedstuff',
            name='sync_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 22, 9, 11, 28, 768183)),
        ),
    ]
