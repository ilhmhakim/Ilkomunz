# Generated by Django 4.2.1 on 2023-05-25 03:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=500)),
                ('user', models.CharField(max_length=100)),
                ('time_created', models.DateTimeField(default=datetime.datetime.now)),
                ('comment', models.TextField()),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='FollowersCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
                ('user_tipe', models.CharField(max_length=100, null=True)),
                ('follower_tipe', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=500)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('image', models.ImageField(default='blank.png', upload_to='post_images')),
                ('caption', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('no_of_likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField(null=True)),
                ('bio', models.TextField(blank=True)),
                ('profileimg', models.ImageField(default='blank.png', upload_to='profile_img')),
                ('nama', models.CharField(blank=True, max_length=100)),
                ('jurusan', models.CharField(blank=True, max_length=100)),
                ('angkatan', models.IntegerField(null=True)),
                ('tipe', models.CharField(default='user', max_length=100)),
                ('buka', models.IntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Presensi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('komun', models.CharField(max_length=100)),
                ('kegiatan', models.CharField(max_length=100)),
            ],
            options={
                'unique_together': {('user', 'komun', 'kegiatan')},
            },
        ),
        migrations.CreateModel(
            name='Pertemuan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('deskripsi', models.TextField(blank=True)),
                ('kegiatan', models.CharField(max_length=100)),
                ('tempat', models.CharField(max_length=100)),
                ('time_created', models.DateTimeField(default=datetime.datetime.now)),
                ('time_end', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'unique_together': {('user', 'kegiatan')},
            },
        ),
    ]
