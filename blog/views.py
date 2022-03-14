from django.shortcuts import render, HttpResponseRedirect
from . forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from . models import Post
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import json

user_model = get_user_model()
# home viewm
def home(request):
    posts = Post.objects.filter(id= 12)
    return render(request, 'blog/home.html', {'posts': posts})

#about
def about(request):
    return render(request, 'blog/about.html')

#contact
def contact(request):
    return render(request, 'blog/contact.html')
    
#dashboard
def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser == True:
            posts = Post.objects.all()
        else:
            posts= Post.objects.filter(uname= user)
    
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html',{'posts': posts, 'full_name': full_name, 'groups': gps})
    else:
        return HttpResponseRedirect('/login/')

#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#signup
def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
           form.save() 
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})
#activate
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = user_model._default_manager.get(pk= uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account activated now you can login')
        return HttpResponseRedirect('/login/')
    else:
        messages.warning(request, 'activation link is invalid')
        return HttpResponseRedirect('/signup/')

#login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                nm = fm.cleaned_data['username']
                psw = fm.cleaned_data['password']
                user = authenticate(username=nm, password=psw)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'User Login Successfully!!')
                    return HttpResponseRedirect('/dashboard/')
                else:
                    messages.error(request, 'wrong user enter correct one')
                    fm = LoginForm()
                    return render(request, 'blog/login.html', {'form': fm})
        else:
            fm = LoginForm()
        return render(request, 'blog/login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/dashboard/')

#add new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                name = request.user
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                add_pst = Post(uname= name, title= title, desc= desc)
                add_pst.save() 
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')    

#update post
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk= id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk= id)
            form = PostForm(instance=pi)
        return HttpResponseRedirect('/dashboard/')
        # return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

#update post
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk= id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

