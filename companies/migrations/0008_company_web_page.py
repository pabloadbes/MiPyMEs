# Generated by Django 5.0.6 on 2024-08-04 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0007_alter_company_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='web_page',
            field=models.CharField(blank=True, null=True, verbose_name='Página web'),
        ),
    ]