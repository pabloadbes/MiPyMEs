# Generated by Django 5.0.6 on 2024-08-03 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_city_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='companies.city', verbose_name='Localidad'),
        ),
    ]