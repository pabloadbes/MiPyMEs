# Generated by Django 5.0.6 on 2024-07-28 21:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0021_rename_subtitle_subsection_and_more'),
        ('surveys', '0021_alter_survey_next_question'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Variable_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Nombre')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado el')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado el')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_list_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('option', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='questions.option', verbose_name='Opción')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_list_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Tabla de variables estadísticas de interés',
                'verbose_name_plural': 'Tabla de variables estadísticas de interés',
                'ordering': ['name', '-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=500, verbose_name='Valor')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado el')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado el')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variables_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('survey', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='surveys.survey', verbose_name='Encuesta')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
                ('variable_list', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='surveys.variable_list', verbose_name='Listado de variables')),
            ],
            options={
                'verbose_name': 'Variable estadística de interés',
                'verbose_name_plural': 'Variables estadísticas de interés',
                'ordering': ['survey', '-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Variable_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('description', models.CharField(max_length=500, verbose_name='Descripción')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado el')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado el')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_type_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_type_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Tipo de variable estadística de interés',
                'verbose_name_plural': 'Tipos de variable estadística de interés',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='variable_list',
            name='variable_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='surveys.variable_type', verbose_name='Tipo de variable'),
        ),
    ]
