# Generated by Django 2.0 on 2018-04-25 02:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projektai', '0017_auto_20180424_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='old_projektas',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 24, 23, 21, 43, 10375, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='old_task',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 24, 23, 21, 43, 11378, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='syncedstuff',
            name='sync_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 24, 23, 21, 43, 8369, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_parent_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
