# Generated by Django 5.0.6 on 2024-06-23 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_type_alter_question_options_alter_section_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Type',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='type',
            new_name='question_type',
        ),
        migrations.AddField(
            model_name='question',
            name='survey_type',
            field=models.IntegerField(default=1, verbose_name='Tipo de Encuesta'),
            preserve_default=False,
        ),
    ]