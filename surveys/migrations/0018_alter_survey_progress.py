# Generated by Django 5.0.6 on 2024-07-15 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0017_alter_survey_next_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='progress',
            field=models.IntegerField(default=0, verbose_name='Progreso'),
        ),
    ]
