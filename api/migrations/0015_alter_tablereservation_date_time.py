# Generated by Django 3.2.9 on 2021-12-15 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20211215_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablereservation',
            name='date_time',
            field=models.DateField(),
        ),
    ]
