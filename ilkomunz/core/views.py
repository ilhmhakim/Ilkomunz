from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .models import Profile,Post,LikePost,FollowersCount, Comment, Pertemuan, Presensi, Artikel, Notification
from itertools import chain
from django.utils import timezone
from datetime import datetime,timedelta
import random

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    
    user_following_list = []
    feed = []
    komun_list = []
    dict = {}
    
    user_following = FollowersCount.objects.filter(follower = request.user.username)
    comment_posts = Comment.objects.all()
    user_komun = FollowersCount.objects.filter(follower_tipe = 'komunitas', user = request.user.username)
    
    for item in user_komun:
        komun_object = User.objects.get(username=item.follower)
        komun_profile = Profile.objects.get(user=komun_object)
        komun_list.append(komun_profile)
    
    user_list_komun = []
    list_komun = Profile.objects.filter(tipe = "komunitas")
    for i in list_komun:
        user_list_komun.append(i.user.username)
    
    for users in user_following:
        user_following_list.append(users.user)
    user_following_list.append(request.user.username)
    
    for usernames in user_following_list:
        feed_object = Post.objects.filter(user = usernames)
        feed.append(feed_object)
        for object in feed_object:
            user_object = User.objects.get(username = object.user)
            dict[object.user] = Profile.objects.get(user = user_object)
            
    komun = list(komun_list)
    feed_list = list(chain(*feed))
    
    return render(request,  'index.html', {'user_profile' : user_profile, 'posts' : feed_list, 'dict' : dict, 'komun' : komun, 'comment_posts' : comment_posts, })

@login_required(login_url='signin')
def riwayatpresensi(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_komun = FollowersCount.objects.filter(follower_tipe = 'komunitas', user = request.user.username)
    
    komun_list = []
    kegiatan_list = []
    
    for item in user_komun:
        komun_object = User.objects.get(username=item.follower)
        komun_profile = Profile.objects.get(user=komun_object)
        komun_list.append(komun_profile)
    
    user_komun = (komun_list[0]).user.username
    if 'user_komun' in request.GET:
        user_komun = request.GET.get('user_komun')
        
    print(user_komun)
    pertemuan_list = Pertemuan.objects.filter(user=user_komun)
    presensi_list = Presensi.objects.filter(user = request.user.username, komun=user_komun)
    for i in presensi_list:
        kegiatan_list.append(i.kegiatan)
    if len(pertemuan_list) == 0:
        percentage = 0
    else:
        percentage = int(100*len(kegiatan_list)/len(pertemuan_list))
    context = {
        'user_profile' : user_profile,
        'komun' : komun_list,   
        'pertemuan_list' : pertemuan_list,   
        'kegiatan_list' : kegiatan_list,
        'percentage' : percentage,
    }
    return render(request, 'riwayatPresensi.html', context)

@login_required(login_url='signin')
def presensipage(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_komun = FollowersCount.objects.filter(follower_tipe = 'komunitas', user = request.user.username)
    
    komun_list = []
    
    for item in user_komun:
        komun_object = User.objects.get(username=item.follower)
        komun_profile = Profile.objects.get(user=komun_object)
        komun_list.append(komun_profile)
    
    if user_profile.tipe == 'komunitas':
        pertemuan_list = Pertemuan.objects.filter(user=request.user.username).order_by('time_created')
        presensi_list = Pertemuan.objects.filter(user=request.user.username)
        
        dict_list = {}
        
        for presensi in presensi_list:
            if len(Presensi.objects.filter(kegiatan=presensi.kegiatan, komun=presensi.user)) > 0:
                dict_list[presensi.kegiatan] = len(Presensi.objects.filter(kegiatan=presensi.kegiatan, komun=presensi.user))
            else:
                dict_list[presensi.kegiatan] = '0'
                
        context = {
            'user_profile' : user_profile,
            'komun' : komun_list,
            'pertemuan_list' : pertemuan_list,
            'length' : len(pertemuan_list),
            'dict' : dict_list
        }
        print(dict_list)
        return render(request, 'presensiSetting.html', context)
    
    
    if (len(komun_list)):
        page = komun_list[0]
    
    context = {
        'user_profile' : user_profile,
        'komun' : komun_list,
    }
    
    if len(komun_list):
        if "user_komun" in request.GET:
            user_komun = request.GET.get('user_komun')
            komun_object = User.objects.get(username=user_komun)
            page = Profile.objects.get(user=komun_object)
        pertemuan_list = Pertemuan.objects.filter(user=page.user.username)
        context['page'] = page
        context['pertemuan_list'] = pertemuan_list
        return render(request, 'presensiPage.html', context)
    else:
        return render(request, 'notpresensi.html', context)
    
def artikelpage(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)    
    user_list = Profile.objects.all()
    artikel_list = Artikel.objects.all()
    artikel_list = list(artikel_list)[::-1]
    artikel = Artikel.objects.latest('created_at')
    
    tema_list = []
    tema_dict = {}
    
    for item in artikel_list:
        if item.tipe in tema_list:
            tema_dict[item.tipe] += 1
        else:
            tema_dict[item.tipe] = 0
            tema_list.append(item.tipe)
    
    tema_dict = dict(sorted(tema_dict.items(), key=lambda x: x[1], reverse=True))
    sorted_tema_list = tema_dict.keys()
    if len(sorted_tema_list) >7:
        sorted_tema_list = sorted_tema_list[:7]
    tema = Artikel.objects.filter(tipe = next(iter(tema_dict)))
    tipe = next(iter(tema_dict))
    
    my_artikel = Artikel.objects.filter(user = request.user.username)
    if len(my_artikel) > 4:
        my_artikel = my_artikel[:4]
    
    if 'id' in request.GET:
        id_artikel = request.GET.get('id')
        artikel = Artikel.objects.get(id_artikel = id_artikel)
        # print(artikel.judul)
        
    if 'tipe_artikel' in request.GET:
        tema = Artikel.objects.filter(tipe = request.GET.get('tipe_artikel'))
        tipe = request.GET.get('tipe_artikel')
    
        
    if 'add' in request.GET:
        cek = request.GET.get('add')
        if cek == 'yes':
            artikel = Artikel.objects.next(artikel)
        elif cek == 'no':
            artikel = Artikel.objects.before(artikel)
            

    if Artikel.objects.before(artikel) == None:
        count = 1
    elif Artikel.objects.next(artikel) == None:
        count = 2
    else:
        count = 0
    
    context = {
        'user_profile' : user_profile,
        'artikel' : artikel,
        'count' : count,
        'tema_list' : sorted_tema_list,
        'tema' : tema,
        'tipe' : tipe,
        'my_artikel' : my_artikel,
        'user_list' : user_list
    }

    print(count)
        
    return render(request, 'openArtikel.html', context)

@login_required(login_url='signin')
def likepost(request):
    username = request.user.username
    user_profile = Profile.objects.get(user = request.user)
    post_id = request.GET.get('post_id')
    pk = request.GET.get('pk')
    
    post = Post.objects.get(id = post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    
    if like_filter == None:
        new_like = LikePost.objects.create(post_id = post_id, username = username)
        new_like.save()
        if post.user != request.user.username:
            new_notif = Notification.objects.create(user_sent = post.user, user_notif = request.user.username, user_notif_image = user_profile.profileimg, tipe="like")
            new_notif.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        # print(pk)
        # print(post.user)
        if pk == post.user:
            return redirect('/profile/'+pk)
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        if pk == post.user:
            return redirect('/profile/'+pk)
        return redirect('/')


@login_required(login_url='signin')        
def artikel(request,pk):
    artikel_content = Artikel.objects.get(id_artikel = pk)
    creator_object = User.objects.get(username=artikel_content.user)
    user_profile = Profile.objects.get(user = request.user)
    artikel_creator = Profile.objects.get(user = creator_object)
    user_komun = FollowersCount.objects.filter(follower_tipe = 'komunitas', user = artikel_content.user)
    
    komun_list = []
    
    for item in user_komun:
        komun_object = User.objects.get(username=item.follower)
        komun_profile = Profile.objects.get(user=komun_object)
        komun_list.append(komun_profile)
    
    context = {
        'user_profile' : user_profile,
        'artikel_creator' : artikel_creator,
        'artikel_content' : artikel_content,
        'komun' : komun_list,
    }
    
    return render(request, 'artikelDalem.html', context)

@login_required(login_url='signin')        
def notification(request):
    user_profile = Profile.objects.get(user = request.user)
    user_komun = FollowersCount.objects.filter(follower_tipe = 'komunitas', user = request.user.username)
    notif_list = Notification.objects.filter(user_sent = request.user.username)
    
    if len(notif_list) > 15:
        notif_list = notif_list[:15]
    
    komun_list = []
    
    for item in user_komun:
        komun_object = User.objects.get(username=item.follower)
        komun_profile = Profile.objects.get(user=komun_object)
        komun_list.append(komun_profile)
        
    context = {
        'user_profile' : user_profile,
        'komun' : komun_list,
        'notif_list' : notif_list,
    }

    return render(request, 'notificationPage.html', context)
    
@login_required(login_url='signin')     
def komunitas(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    all_komunitas = Profile.objects.filter(tipe = "komunitas")
    all_komunitas1 = all_komunitas[len(all_komunitas)//2:]
    all_komunitas2 = all_komunitas[:len(all_komunitas)//2]
    user_komun = FollowersCount.objects.filter(follower_tipe = 'komunitas', user = request.user.username)
    follower_komun = FollowersCount.objects.filter(user_tipe = 'komunitas', follower = request.user.username)
    
    komun_list = []
    komun_join_list = []
    komun_follower_list = []
    
    for item in user_komun:
        komun_object = User.objects.get(username=item.follower)
        komun_profile = Profile.objects.get(user=komun_object)
        komun_list.append(komun_profile)
        komun_join_list.append(item.follower)
    
    for i in follower_komun:
        komun_follower_list.append(i.user)
    
    context = {
        'user_profile' : user_profile,
        'komun' : komun_list,
        'all_komun' : all_komunitas1,
        'all_komun2' : all_komunitas2,
        'komun_follower' : komun_follower_list,
        'komun_join' : komun_join_list,
    }
    # print(komun_follower_list)
    # print(komun_join_list)
    return render(request,'komunitas.html', context)   
    
@login_required(login_url='signin')        
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user = user_object)
    user_posts = Post.objects.filter(user = pk)
    user_post_length = len(user_posts)
    
    follower = request.user.username
    user = pk
    follower_object = User.objects.get(username = follower)
    follower_profile = Profile.objects.get(user = follower_object)
    
    if FollowersCount.objects.filter(follower = follower, user = user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    
    count = FollowersCount.objects.filter(follower = user, user = follower).first()
    
    user_follower = len(FollowersCount.objects.filter(user = pk))
    user_following = len(FollowersCount.objects.filter(follower = pk))
    comment_posts = Comment.objects.all()
    
    context = {
        'user_object' : user_object,
        'user_profile' : user_profile,
        'follower_profile' : follower_profile,
        'user_posts' : user_posts,
        'user_post_length' : user_post_length,
        'button_text' : button_text,
        'user_following' : user_following,
        'user_follower' : user_follower,
        'tes' : count,
        'comment_posts' : comment_posts,
    }
    if follower == pk:
        user_follower = []
        not_follower = []
        
        all_user = Profile.objects.all()
        follower_list = FollowersCount.objects.filter(user = follower)
        for i in follower_list:
            user_follower.append(i.follower)
        for i in all_user:
            if i.user.username in follower_list or i.user.username == follower or i.tipe == 'komunitas':
                continue
            not_follower.append(i)
        random.shuffle(not_follower)
        if len(not_follower) > 3:
            context['not_follower'] = not_follower[:3]
        else:
            context['not_follower'] = not_follower
        return render(request,'myprofile.html', context)
    else:
        artikel_list = Artikel.objects.filter(user = pk)
        if len(artikel_list) > 3:
            artikel_list = artikel_list[:3]
        context['artikel_list'] = artikel_list
        return render(request,'profile.html', context)
        

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_komun = FollowersCount.objects.filter(follower_tipe = 'komunitas', user = request.user.username)
    
    komun_list = []
    
    for item in user_komun:
        komun_object = User.objects.get(username=item.follower)
        komun_profile = Profile.objects.get(user=komun_object)
        komun_list.append(komun_profile)
    # username_profile = []
    username_profile_list = []
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains = username)
        
        for users in username_object:
            if users.username == 'admin':
                continue
            # print(users.username)
            search_profile = Profile.objects.get(user=users) 
            username_profile_list.append(search_profile)
            
        # for ids in username_profile:
        #     profile_lists = Profile.objects.filter(id_user = ids)
        #     username_profile_list.append(profile_lists)
    if len(username_profile_list) > 15:
        username_profile_list = username_profile_list[:15]
    return render(request,'hasilPencarian.html', {'user_profile': user_profile, 'username_profile_list' : username_profile_list, 'komun': komun_list})

@login_required(login_url='signin')
def searchartikel(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_komun = FollowersCount.objects.filter(follower_tipe = 'komunitas', user = request.user.username)
    
    komun_list = []
    
    for item in user_komun:
        komun_object = User.objects.get(username=item.follower)
        komun_profile = Profile.objects.get(user=komun_object)
        komun_list.append(komun_profile)
    # username_profile = []
    username_profile_list = []
    if request.method == 'POST':
        username = request.POST['username']
        artikel_list = Artikel.objects.filter(Q(judul__icontains=username) | Q(tipe__icontains=username))
        
        # for users in username_object:
        #     if users.username == 'admin':
        #         continue
        #     # print(users.username)
        #     search_profile = Profile.objects.get(user=users) 
        #     username_profile_list.append(search_profile)
            
        # for ids in username_profile:
        #     profile_lists = Profile.objects.filter(id_user = ids)
        #     username_profile_list.append(profile_lists)
    if len(artikel_list) > 15:
        artikel_list = artikel_list[:15]
    return render(request,'hasilPencarianArtikel.html', {'user_profile': user_profile, 'artikel_list' : artikel_list, 'komun': komun_list})

@login_required(login_url='signin')
def comment(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        pk = request.POST['pk']
        comment = request.POST['content']
        post = Post.objects.get(id = post_id)    
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user = user_object)
        new_comment = Comment.objects.create(post_id = post_id, user = pk, comment = comment, img = user_profile.profileimg)
        new_comment.save()
        if post.user != request.user.username:
            new_notif = Notification.objects.create(user_sent = post.user, user_notif = request.user.username, user_notif_image = user_profile.profileimg, tipe="comment")
            new_notif.save()
        
    comment_posts = Comment.objects.filter(post_id = post_id)
    
    context = {
        'comment_posts' : comment_posts,
        'post_id' : post_id,
        'pk' : pk,
        'post' : post,
    }
    
    if 'cek' in request.POST:
        cek = request.POST['cek']
        return redirect('/profile/' + cek)
    else:
        return redirect('/')


@login_required(login_url='signin')
def uploadartikel(request):
    if request.method == 'POST':
        user = request.user.username
        content = request.POST['isiartikel']
        judul = request.POST['judul']
        tipe = request.POST['tipe_artikel']
        
        user_object = User.objects.get(username = request.user.username)
        user_profile = Profile.objects.get(user=user_object)
        follower_list = FollowersCount.objects.filter(user = user)
        
        if request.FILES.get('imgartikel') == None:
            new_artikel = Artikel.objects.create(user = user, content = content, judul = judul, tipe = tipe)
            new_artikel.save()
            
            for item in follower_list:
                new_notif = Notification.objects.create(user_sent = item.follower, user_notif = user, user_notif_image = user_profile.profileimg, tipe="artikel",id_tipe = new_artikel.id_artikel)
                new_notif.save()
    
            return redirect('/')
        else:
            image = request.FILES.get('imgartikel')
            new_artikel = Artikel.objects.create(user = user,image=image, content = content, judul = judul, tipe = tipe)
            new_artikel.save()
            
            for item in follower_list:
                new_notif = Notification.objects.create(user_sent = item.follower, user_notif = user, user_notif_image = user_profile.profileimg, tipe="artikel",id_tipe = new_artikel.id_artikel)
                new_notif.save()
            
            return redirect('/')

@login_required(login_url='signin')
def delete(request):
    if request.method == "GET":
        id = request.GET.get('id')
        post = Post.objects.get(id = id)
        post.delete()
        comment_list = Comment.objects.filter(post_id=id)
        for item in comment_list:
            item.delete()
        if 'cek' in request.GET:
            cek = request.GET.get('cek')
            return redirect('/profile/'+cek)
        return redirect('/')
    else:
        return redirect('/')
    

@login_required(login_url='signin')
def upload(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        if 'cek' in request.POST:
            cek = request.POST['cek']
            return redirect('/profile/' + cek)
        else:
            return redirect('/')
    else:
        if 'cek' in request.POST:
            cek = request.POST['cek']
            return redirect('/profile/' + cek)
        else:
            return redirect('/')


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        user_object = User.objects.get(username=follower)
        user_follower = Profile.objects.get(user = user_object)
        user_object = User.objects.get(username=user)
        user_user = Profile.objects.get(user = user_object)
        
        if FollowersCount.objects.filter(follower=follower, user = user):
            delete_follower = FollowersCount.objects.get(follower=follower, user = user, user_tipe = user_user.tipe, follower_tipe = user_follower.tipe)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user = user, user_tipe = user_user.tipe, follower_tipe = user_follower.tipe)
            new_follower.save()
            new_notif = Notification.objects.create(user_sent = user, user_notif = request.user.username, user_notif_image = user_follower.profileimg, tipe="follow")
            new_notif.save()
            return redirect('/profile/'+user)
        
    else:
        return redirect('/profile/'+user)
    
@login_required(login_url='signin')
def daftar(request):
    # follower = request.POST['buka']
    user = request.user.username
    user_object = User.objects.get(username=user)
    user_profile = Profile.objects.get(user = user_object)
    
    if user_profile.buka == 0:
        user_profile.buka = 1
        user_profile.save()
        return redirect('/profile/'+user)
    else:
        user_profile.buka = 0
        user_profile.save()
        return redirect('/profile/'+user)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if User.objects.filter(email = email).exists():
            messages.info(request, 'Email Taken')
            return redirect('signup')
        elif password != password2:
            messages.info(request, 'Password Tidak Sama')
            return redirect('signup')
        elif "@apps.ipb.ac.id" not in email:
            messages.info(request, 'You Must Use IPB Email')
            return redirect('signup')
        elif User.objects.filter(username = username).exists():
            messages.info(request, 'Username Taken')
            return redirect('signup')
        else:
            user = User.objects.create_user(username = username, email = email, password=password)
            user.save()
            
            #redirect to settings page
            user_login = auth.authenticate(username  = username, password = password)
            auth.login(request, user_login)
            
            #create profile object
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model,id_user = user_model.id)
            new_profile.save()
            return redirect('settings')

    else:    
        return render(request, 'registerPage.html')
    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username = username, password = password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid user')
            return redirect('signin')
    else:
        return render(request, 'loginPage.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def presensi(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            kegiatan = request.POST['kegiatan']
            user = request.user.username
            komun = request.POST['komun']
            
            pertemuan = Pertemuan.objects.get(user=komun, kegiatan = kegiatan)
            if timezone.now() > pertemuan.time_end:
                messages.info(request, 'Waktu Presensi Sudah Lewat')
                return redirect('/presensipage')
            
            new_notif = Notification.objects.create(user_sent = komun, user_notif = request.user.username, user_notif_image = user_profile.profileimg, tipe="presensi")
            new_notif.save()
            
            new_presensi= Presensi.objects.create(user = user, komun = komun, kegiatan = kegiatan)
            # print(user,komun,kegiatan)
            # print(new_presensi.user,new_presensi.komun,new_presensi.kegiatan)
            new_presensi.save()
            
            return redirect('/presensipage')
        except:
            messages.info(request, 'Anda Sudah Melakukan Presensi')
            return redirect('/presensipage')
    else:
        print(user_profile.user)
        return redirect('/presensipage')
        
        

@login_required(login_url='signin')
def presensiadd(request):
    user_profile = Profile.objects.get(user=request.user)
    user_komun = FollowersCount.objects.filter(follower_tipe = 'komunitas', user = request.user.username)
    if user_profile.tipe != 'komunitas':
        return redirect('/')
    
    komun_list = []
    
    for item in user_komun:
        komun_object = User.objects.get(username=item.follower)
        komun_profile = Profile.objects.get(user=komun_object)
        komun_list.append(komun_profile)
    
    context = {
        'user_profile' : user_profile,
        'komun' : komun_list,
    }
    
    if request.method == 'POST':
        try:
            user = user_profile.user.username
            deskripsi = request.POST['deskripsi']
            kegiatan = request.POST['name']
            tempat = request.POST['tempat']
            jam = int(request.POST['jam'])
            menit = int(request.POST['menit'])
            
            time_delta = timedelta(hours=jam, minutes=menit)
            time_end = datetime.now()+time_delta
            new_pertemuan = Pertemuan.objects.create(user=user,deskripsi=deskripsi,kegiatan =kegiatan, tempat = tempat, time_end = time_end)    

            new_pertemuan.save()   
            return redirect('/presensipage')
        except:
            messages.info(request, 'Nama Kegiatan Harus Unik')
            return render(request, 'setpresensi.html', context)   
 
    else:
        return render(request, 'isiPresensi.html', context)   
         

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            nama = request.POST['name']
            angkatan = request.POST['angkatan']
            jurusan = request.POST['jurusan']

            user_profile.profileimg = image
            user_profile.bio = bio            
            user_profile.nama = nama            
            user_profile.angkatan = angkatan            
            user_profile.jurusan = jurusan     
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            nama = request.POST['name']
            angkatan = request.POST['angkatan']
            jurusan = request.POST['jurusan']

            user_profile.profileimg = image
            user_profile.bio = bio            
            user_profile.nama = nama            
            user_profile.angkatan = angkatan            
            user_profile.jurusan = jurusan     
            user_profile.save()
        
    if 'cek' in request.POST:
        cek = request.POST['cek']
        return redirect('/profile/' + cek)
    else:
        return redirect('/')

def editsampul(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        if request.FILES.get('sampul') != None:
            image = request.FILES.get('sampul')
            user_profile.sampulimg = image
            user_profile.save()
            return redirect('/profile/'+request.user.username)
            