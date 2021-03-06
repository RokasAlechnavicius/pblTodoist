# Generated by Django 2.0 on 2018-04-20 12:19

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projektai', '0008_auto_20180420_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='old_projektas',
            name='Parent_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='old_projektas',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 20, 15, 19, 4, 429224)),
        ),
        migrations.AlterField(
            model_name='old_task',
            name='task_parent_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='old_task',
            name='task_project_id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='old_task',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 20, 15, 19, 4, 429726)),
        ),
        migrations.AlterField(
            model_name='syncedstuff',
            name='sync_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 20, 15, 19, 4, 426703)),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='projektai.Task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projektai.Projektas'),
        ),
    ]
