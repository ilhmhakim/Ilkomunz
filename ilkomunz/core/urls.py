from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('signup', views.signup, name = 'signup'),
    path('signin', views.signin, name = 'signin'),
    path('logout', views.logout, name = 'logout'),
    path('settings', views.settings, name = 'settings'),
    path('editsampul', views.editsampul, name = 'editsampul'),
    path('profile/settings', views.settings, name = 'settings'),
    path('notification', views.notification, name = 'notification'),
    path('search', views.search, name = 'search'),
    path('searchartikel', views.searchartikel, name = 'searchartikel'),
    path('upload', views.upload, name = 'upload'),
    path('delete', views.delete, name = 'delete'),
    path('presensipage', views.presensipage, name = 'presensipage'),
    path('presensiadd', views.presensiadd, name = 'presensiadd'),
    path('presensi', views.presensi, name = 'presensi'),
    path('riwayatpresensi', views.riwayatpresensi, name = 'riwayatpresensi'),
    path('uploadartikel', views.uploadartikel, name = 'uploadartikel'),
    path('artikelpage', views.artikelpage, name = 'artikelpage'),
    path('profile/<str:pk>', views.profile, name = 'profile'), 
    path('komunitas', views.komunitas, name = 'komunitas'), 
    path('artikel/<str:pk>', views.artikel, name = 'artikel'), 
    path('comment', views.comment, name = 'comment'), 
    path('likepost', views.likepost, name = 'likepost'),
    path('follow', views.follow, name = 'follow'),
    path('daftar', views.daftar, name = 'daftar'),
]
