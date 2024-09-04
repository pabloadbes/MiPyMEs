# Generated by Django 5.0.6 on 2024-08-30 04:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0027_delete_filter_type'),
        ('surveys', '0028_survey_questions_survey_question_state'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado el')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado el')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='questions.question', verbose_name='pregunta')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
                ('variables', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='surveys.variable', verbose_name='Variable')),
            ],
        ),
        migrations.CreateModel(
            name='Filter_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='nombre')),
                ('description', models.CharField(max_length=500, verbose_name='Descripción')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado el')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado el')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_type_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_type_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Tipo de pregunta',
                'verbose_name_plural': 'Tipos de pregunta',
                'ordering': ['name'],
            },
        ),
    ]