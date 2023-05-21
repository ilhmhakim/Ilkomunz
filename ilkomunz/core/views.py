from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .models import Profile,Post,LikePost,FollowersCount
from itertools import chain

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    user_following_list = []
    feed = []
    dict = {}
    
    user_following = FollowersCount.objects.filter(follower = request.user.username)
    
    for users in user_following:
        user_following_list.append(users.user)
    user_following_list.append(request.user.username)
    
    for usernames in user_following_list:
        feed_object = Post.objects.filter(user = usernames)
        feed.append(feed_object)
        for object in feed_object:
            user_object = User.objects.get(username = object.user)
            dict[object.user] = Profile.objects.get(user = user_object)
            
    #     dict[usernames] = Profile.objects.filter(user = usernames).first()
    
    # dict[request.user.username] = Profile.objects.filter(user=request.user.username).first()
    
    feed_list = list(chain(*feed))
    
    #posts = Post.objects.all()
    return render(request,  'index.html', {'user_profile' : user_profile, 'posts' : feed_list, 'dict' : dict})

@login_required(login_url='signin')
def likepost(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Post.objects.get(id = post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    
    if like_filter == None:
        new_like = LikePost.objects.create(post_id = post_id, username = username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')


@login_required(login_url='signin')        
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user = user_object)
    user_posts = Post.objects.filter(user = pk)
    user_post_length = len(user_posts)
    
    follower = request.user.username
    user = pk
    
    if FollowersCount.objects.filter(follower = follower, user = user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    
    user_follower = len(FollowersCount.objects.filter(user = pk))
    user_following = len(FollowersCount.objects.filter(follower = pk))
    
    context = {
        'user_object' : user_object,
        'user_profile' : user_profile,
        'user_posts' : user_posts,
        'user_post_length' : user_post_length,
        'button_text' : button_text,
        'user_following' : user_following,
        'user_follower' : user_follower,
    }
    return render(request,'profile.html', context)

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    username_profile = []
    username_profile_list = []
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains = username)
        
        for users in username_object:
            username_profile.append(users.id)
            
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user = ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return  render(request,'search.html', {'user_profile': user_profile, 'username_profile_list' : username_profile_list})

@login_required(login_url='signin')
def upload(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        
        if FollowersCount.objects.filter(follower=follower, user = user):
            delete_follower = FollowersCount.objects.get(follower=follower, user = user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower = follower, user = user)
            new_follower.save()
            return redirect('/profile/'+user)
        
    else:
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
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            print("tes")
            print("tes")
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
        
        return redirect('settings')
            
    
    return render(request, 'setting.html',{'user_profile' : user_profile})