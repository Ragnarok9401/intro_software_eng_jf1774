# Generated by Django 4.2.5 on 2023-10-25 18:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bark',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 25, 18, 56, 19, 920599, tzinfo=datetime.timezone.utc)),
        ),
    ]
