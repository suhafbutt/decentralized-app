# Generated by Django 5.0.4 on 2024-05-11 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0004_alter_song_link_alter_user_storage_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='is_trusted',
            field=models.BooleanField(default=True),
        ),
    ]