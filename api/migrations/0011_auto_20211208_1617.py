# Generated by Django 3.2.9 on 2021-12-08 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_order_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='is_reserved',
        ),
        migrations.AddField(
            model_name='table',
            name='num_of_chairs',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
