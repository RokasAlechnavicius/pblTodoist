# Generated by Django 2.0 on 2018-05-09 17:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projektai', '0037_auto_20180509_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='old_projektas',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 9, 14, 15, 38, 788796, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='old_task',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 9, 14, 15, 38, 789799, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='syncedstuff',
            name='sync_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 9, 14, 15, 38, 786791, tzinfo=utc)),
        ),
    ]
