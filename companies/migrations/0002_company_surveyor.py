# Generated by Django 5.0.6 on 2024-07-20 03:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        ('team', '0003_supervisor_created_supervisor_updated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='surveyor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='team.surveyor', verbose_name='Encuestador Asignado'),
        ),
    ]
