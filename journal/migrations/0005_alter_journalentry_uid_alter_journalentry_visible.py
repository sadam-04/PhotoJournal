# Generated by Django 5.1.6 on 2025-02-28 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0004_journalentry_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='uid',
            field=models.UUIDField(auto_created=True, unique=True),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
