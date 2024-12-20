# Generated by Django 5.0.7 on 2024-10-14 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0019_alter_company_inactive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address_number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Número / Km'),
        ),
        migrations.AlterField(
            model_name='company',
            name='dept',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Departamento'),
        ),
        migrations.AlterField(
            model_name='company',
            name='sector',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Sector'),
        ),
    ]
