# Generated by Django 2.0 on 2018-04-09 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='token',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]