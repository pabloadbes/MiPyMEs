# Generated by Django 5.0.6 on 2024-08-29 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0026_survey_question_state'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='survey_question_state',
            options={'ordering': ['name'], 'verbose_name': 'Estado de preguntas de la encuesta', 'verbose_name_plural': 'Estados de preguntas de la encuesta'},
        ),
    ]
