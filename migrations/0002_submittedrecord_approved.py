# Generated by Django 5.0.6 on 2024-07-10 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submittedrecord',
            name='approved',
            field=models.BooleanField(default=None),
        ),
    ]
