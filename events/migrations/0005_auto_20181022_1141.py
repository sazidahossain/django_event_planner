# Generated by Django 2.1 on 2018-10-22 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20181022_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='seats_left',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='seats',
            field=models.IntegerField(default=0),
        ),
    ]
