# Generated by Django 5.0.6 on 2024-06-22 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_alter_question_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Type',
            new_name='Question_Type',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='type',
            new_name='question_type',
        ),
        migrations.AddField(
            model_name='question',
            name='survey_type',
            field=models.CharField(default='s', verbose_name='Tipo Encuesta'),
            preserve_default=False,
        ),
    ]
