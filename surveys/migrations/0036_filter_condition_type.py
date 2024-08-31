# Generated by Django 5.0.6 on 2024-08-30 23:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0035_condition_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='condition_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='surveys.condition_type', verbose_name='Condición'),
            preserve_default=False,
        ),
    ]
