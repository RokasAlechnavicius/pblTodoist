# Generated by Django 2.0.4 on 2018-04-25 12:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projektai', '0019_auto_20180425_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='old_projektas',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 25, 12, 42, 40, 613926, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='old_task',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 25, 12, 42, 40, 614646, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='syncedstuff',
            name='sync_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 25, 12, 42, 40, 611573, tzinfo=utc)),
        ),
    ]
