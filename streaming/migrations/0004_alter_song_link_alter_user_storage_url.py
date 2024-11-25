# Generated by Django 5.0.4 on 2024-05-09 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0003_song_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='link',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='storage_url',
            field=models.TextField(unique=True),
        ),
    ]