# Generated by Django 5.0.6 on 2024-08-30 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0032_filter_value_alter_filter_variables'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='dest',
            field=models.IntegerField(default=1, verbose_name='Destino'),
            preserve_default=False,
        ),
    ]