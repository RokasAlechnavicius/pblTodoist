# Generated by Django 2.0 on 2018-04-22 09:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projektai', '0015_auto_20180422_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='old_projektas',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 22, 6, 15, 28, 87930, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='old_task',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 22, 6, 15, 28, 87930, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='syncedstuff',
            name='sync_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 22, 6, 15, 28, 85926, tzinfo=utc)),
        ),
    ]