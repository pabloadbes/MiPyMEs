# Generated by Django 5.0.6 on 2024-08-26 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='CALLE',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Calle'),
        ),
        migrations.AlterField(
            model_name='result',
            name='CODEMP',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Código de Empresa'),
        ),
        migrations.AlterField(
            model_name='result',
            name='CUIT',
            field=models.CharField(max_length=11, verbose_name='CUIT'),
        ),
        migrations.AlterField(
            model_name='result',
            name='NUMERO',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Número'),
        ),
        migrations.AlterField(
            model_name='result',
            name='RAZON',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Razón Social'),
        ),
    ]