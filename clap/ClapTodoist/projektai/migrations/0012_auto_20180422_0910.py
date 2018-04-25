# Generated by Django 2.0 on 2018-04-22 06:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180419_0227'),
        ('projektai', '0011_auto_20180421_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='old_task',
            name='Project_token',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.UserProfile', to_field='token'),
        ),
        migrations.AlterField(
            model_name='old_projektas',
            name='Project_token',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.UserProfile', to_field='token'),
        ),
        migrations.AlterField(
            model_name='old_projektas',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 22, 9, 10, 5, 454352)),
        ),
        migrations.AlterField(
            model_name='old_task',
            name='when_deleted',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 22, 9, 10, 5, 455326)),
        ),
        migrations.AlterField(
            model_name='syncedstuff',
            name='sync_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 22, 9, 10, 5, 452346)),
        ),
    ]
