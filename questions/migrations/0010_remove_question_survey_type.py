# Generated by Django 5.0.6 on 2024-06-24 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_alter_question_question_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='survey_type',
        ),
    ]