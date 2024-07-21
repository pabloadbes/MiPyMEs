# Generated by Django 5.0.6 on 2024-07-21 21:10

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0018_alter_survey_progress'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='response',
            options={'ordering': ['survey', '-updated_at'], 'verbose_name': 'respuesta', 'verbose_name_plural': 'respuestas'},
        ),
        migrations.AlterModelOptions(
            name='survey',
            options={'ordering': ['-updated_at', 'company'], 'verbose_name': 'encuesta', 'verbose_name_plural': 'encuestas'},
        ),
        migrations.RemoveField(
            model_name='response',
            name='created',
        ),
        migrations.RemoveField(
            model_name='response',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='created',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='survey_state',
            name='created',
        ),
        migrations.RemoveField(
            model_name='survey_state',
            name='updated',
        ),
        migrations.AddField(
            model_name='response',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado el'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='response',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='response_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='response',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado el'),
        ),
        migrations.AddField(
            model_name='response',
            name='updated_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='response_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado el'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='survey_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado el'),
        ),
        migrations.AddField(
            model_name='survey',
            name='updated_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='survey_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey_state',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creado el'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey_state',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='survey_state_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey_state',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado el'),
        ),
        migrations.AddField(
            model_name='survey_state',
            name='updated_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='survey_state_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por'),
            preserve_default=False,
        ),
    ]
