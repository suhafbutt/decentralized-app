# Generated by Django 5.0.4 on 2024-05-07 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='thumbnail',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
