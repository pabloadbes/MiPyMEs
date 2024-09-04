# Generated by Django 5.0.6 on 2024-08-26 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0003_alter_result_cod_post_alter_result_depto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='DEPTO_LP',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Departamento del Principal Local Productivo'),
        ),
        migrations.AlterField(
            model_name='result',
            name='LOCAL_LP',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Localidad del Principal Local Productivo'),
        ),
        migrations.AlterField(
            model_name='result',
            name='PROV_LP',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Provincia del Principal Local Productivo'),
        ),
    ]