# Generated by Django 3.2.9 on 2021-12-17 07:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20211216_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customization', models.SmallIntegerField(choices=[(0, 'Extra Spicy'), (1, 'Extra Sweet'), (2, 'Extra Meat'), (3, 'Extra Garlic'), (4, 'Extra Cheese')], default=None, null=True)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.food')),
            ],
        ),
        migrations.AlterField(
            model_name='tablereservation',
            name='check_in',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 17, 12, 52, 27, 431658)),
        ),
        migrations.AlterField(
            model_name='tablereservation',
            name='check_out',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 17, 12, 52, 27, 432658)),
        ),
        migrations.CreateModel(
            name='OrderCustomization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customization', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.customization')),
                ('ordered_food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.orderedfood')),
            ],
        ),
    ]
