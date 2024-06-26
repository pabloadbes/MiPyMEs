# Generated by Django 5.0.6 on 2024-06-27 22:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0007_survey_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='progress',
            field=models.IntegerField(default=0, verbose_name='Progreso'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='survey_state',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='surveys.survey_state', verbose_name='Estado de la Encuesta'),
        ),
    ]
