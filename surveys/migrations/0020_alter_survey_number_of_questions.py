# Generated by Django 5.0.6 on 2024-07-22 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0019_alter_response_options_alter_survey_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='number_of_questions',
            field=models.IntegerField(default=0, verbose_name='Cantidad de preguntas'),
        ),
    ]
