# Generated by Django 5.0.4 on 2024-05-05 12:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage_url', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField()),
                ('artist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='streaming.user')),
            ],
        ),
    ]
