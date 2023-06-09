# Generated by Django 4.2.1 on 2023-05-25 03:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artikel',
            fields=[
                ('id_artikel', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('image', models.ImageField(default='blank.png', upload_to='article_images')),
                ('judul', models.CharField(max_length=500)),
                ('tipe', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
