# Generated by Django 5.0.6 on 2024-07-22 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0020_alter_survey_number_of_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='next_question',
            field=models.IntegerField(default=0, verbose_name='Pregunta siguiente'),
        ),
    ]
