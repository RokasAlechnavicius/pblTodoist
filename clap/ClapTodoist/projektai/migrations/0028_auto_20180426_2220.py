# Generated by Django 2.0 on 2018-04-26 22:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projektai', '0027_auto_20180426_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='old_projektas',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 26, 19, 20, 24, 700965, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='old_task',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 26, 19, 20, 24, 701966, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='syncedstuff',
            name='sync_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 26, 19, 20, 24, 698960, tzinfo=utc)),
        ),
    ]
