# Generated by Django 2.0 on 2018-04-14 14:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projektai', '0002_old_task_when_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='old_projektas',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 14, 17, 56, 59, 276054)),
        ),
        migrations.AlterField(
            model_name='old_task',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 14, 17, 56, 59, 277056)),
        ),
    ]
