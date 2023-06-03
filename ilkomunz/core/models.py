from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

class BeforeNextObjectManager(models.Manager):
    def next(self, current_object):
        try:
            return self.get_queryset().filter(created_at__lt=current_object.created_at).order_by('-created_at').first()
        except self.model.DoesNotExist:
            return None
    
    def before(self, current_object):
        try:
            return self.get_queryset().filter(created_at__gt=current_object.created_at).order_by('created_at').first()
        except self.model.DoesNotExist:
            return None
        
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(null = True)
    bio = models.TextField(blank = True)
    profileimg = models.ImageField(upload_to='profile_img', default= 'blank.png')
    sampulimg = models.ImageField(upload_to='sampul_img', default= 'sampul.png')
    nama = models.CharField(max_length=100, blank = True)
    jurusan = models.CharField(max_length=100, blank = True)
    angkatan = models.IntegerField(null = True)
    tipe = models.CharField(max_length=100, default = 'user')
    buka = models.IntegerField(null = True)
    
    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images',default='blank.png')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length = 500)
    username = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.username
    
class FollowersCount(models.Model):
    follower = models.CharField(max_length = 100)
    user = models.CharField(max_length = 100)
    user_tipe = models.CharField(max_length = 100, null = True)
    follower_tipe = models.CharField(max_length = 100, null = True)
    
    def __str__(self):
        return self.user

class Comment(models.Model):
    post_id = models.CharField(max_length = 500) 
    user = models.CharField(max_length = 100)
    time_created = models.DateTimeField(default=datetime.now)
    comment = models.TextField()
    img = models.ImageField()
    def __str__(self):
        return self.post_id
    
class Pertemuan(models.Model):
    user = models.CharField(max_length = 100)
    deskripsi = models.TextField(blank = True)
    kegiatan = models.CharField(max_length = 100) 
    tempat = models.CharField(max_length = 100) 
    time_created = models.DateTimeField(default=datetime.now)
    time_end = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.kegiatan
    
    class Meta:
        unique_together = ('user', 'kegiatan')

class Presensi(models.Model):
    user = models.CharField(max_length = 100)
    komun = models.CharField(max_length = 100)
    kegiatan = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.user
    
    class Meta:
        unique_together = ('user', 'komun', 'kegiatan')
    
class Artikel(models.Model):
    id_artikel = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='article_images', default="blank.png")
    judul = models.CharField(max_length=500)
    tipe = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    objects = BeforeNextObjectManager()
    
    def __str__(self):
        return self.user
    
class Notification(models.Model):
    user_sent = models.CharField(max_length=100)
    user_notif = models.CharField(max_length=100)
    user_notif_image = models.ImageField()
    tipe = models.CharField(max_length=100)
    id_tipe = models.CharField(null = True, max_length = 500, default = None)
    created_at = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.user_sent