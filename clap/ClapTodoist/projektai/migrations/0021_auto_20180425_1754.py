# Generated by Django 2.0.4 on 2018-04-25 17:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projektai', '0020_auto_20180425_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='old_projektas',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 25, 17, 54, 35, 552532, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='old_task',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 25, 17, 54, 35, 553210, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='syncedstuff',
            name='sync_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 25, 17, 54, 35, 550059, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_responsible_uid',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_uid',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
