# Generated by Django 5.0.6 on 2024-06-15 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Razón Social')),
                ('cuit', models.CharField(default='', max_length=13, verbose_name='CUIT')),
                ('clanae_code', models.CharField(max_length=6, verbose_name='CLANAE')),
                ('address_street', models.CharField(max_length=100, verbose_name='Calle / Ruta')),
                ('address_number', models.CharField(max_length=100, verbose_name='Número / Km')),
                ('city', models.CharField(max_length=100, verbose_name='Localidad')),
                ('district', models.CharField(max_length=100, verbose_name='Departamento')),
                ('zip_code', models.CharField(max_length=4, verbose_name='Código Postal')),
                ('phone', models.CharField(max_length=12, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de última modificación')),
            ],
            options={
                'verbose_name': 'empresa',
                'verbose_name_plural': 'empresas',
                'ordering': ['name', 'created'],
            },
        ),
    ]
