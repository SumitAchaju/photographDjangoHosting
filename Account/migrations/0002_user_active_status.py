# Generated by Django 4.1.2 on 2023-09-11 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active_status',
            field=models.BooleanField(default=False),
        ),
    ]
