# Generated by Django 5.0.6 on 2024-06-24 00:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_alter_question_question_type'),
        ('surveys', '0003_delete_survey_type_survey_survey_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='survey_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='questions.survey_type', verbose_name='Tipo de Encuesta'),
        ),
    ]
