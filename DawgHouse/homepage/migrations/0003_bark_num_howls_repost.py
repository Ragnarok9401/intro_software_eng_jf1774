# Generated by Django 4.2.5 on 2023-10-28 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='bark',
            name='num_howls',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Repost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.bark')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
