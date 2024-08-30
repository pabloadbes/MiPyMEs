# Generated by Django 5.0.6 on 2024-08-30 04:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0031_alter_filter_options_alter_filter_type_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='value',
            field=models.IntegerField(default=1, verbose_name='Valor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filter',
            name='variables',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='surveys.variable_list', verbose_name='Variable'),
        ),
    ]
