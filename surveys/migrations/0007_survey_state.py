# Generated by Django 5.0.6 on 2024-06-27 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0006_alter_survey_survey_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey_State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('description', models.CharField(max_length=500, verbose_name='Descripción')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
            ],
        ),
    ]
