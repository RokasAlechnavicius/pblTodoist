# Generated by Django 2.0 on 2018-04-25 22:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projektai', '0022_auto_20180425_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='old_projektas',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 25, 22, 35, 38, 524085, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='old_task',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 25, 22, 35, 38, 524586, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='syncedstuff',
            name='sync_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 25, 22, 35, 38, 522079, tzinfo=utc)),
        ),
    ]
