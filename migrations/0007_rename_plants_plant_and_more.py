# Generated by Django 5.0.6 on 2024-07-11 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0006_plants'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Plants',
            new_name='Plant',
        ),
        migrations.RemoveField(
            model_name='submittedrecord',
            name='file_sizes',
        ),
        migrations.AddField(
            model_name='submittedrecord',
            name='file_urls',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='submittedrecord',
            name='file_names',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
