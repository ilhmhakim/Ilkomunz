from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount, Comment, Pertemuan, Presensi, Artikel, Notification

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Comment)
admin.site.register(Presensi)
admin.site.register(Pertemuan)
admin.site.register(Artikel)
admin.site.register(Notification)