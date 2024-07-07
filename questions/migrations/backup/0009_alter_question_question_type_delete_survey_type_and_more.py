# Generated by Django 5.0.6 on 2024-06-22 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_alter_question_survey_type'),
        ('surveys', '0005_alter_survey_survey_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.IntegerField(verbose_name='Tipo'),
        ),
        migrations.DeleteModel(
            name='Survey_Type',
        ),
        migrations.DeleteModel(
            name='Question_Type',
        ),
    ]