from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from account.forms import PostForm
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from account.models import Post
from pathlib import Path
import cv2
import pathlib
BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('/')

def reg_view(request):

    if request.method == 'POST':
        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print(request.POST)
            form.save()
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            login_user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if login_user:
                login(request, login_user)
                return redirect('/')
 
    
    else:
    
        form = UserCreationForm()
    

    return render(request, 'accounts/reg.html', {'form': form})

def login_view(request):

    if request.method == 'POST':
        
        form = request.POST
       
            
        
      
        password = form.get('password1')
        login_user = authenticate(username=form['username'], password=form['password1'])
        if login_user is not None:
            login(request, login_user)
            return redirect('/')
        
    else:
        print(request.POST)
        form = UserCreationForm()
    

    return render(request, 'accounts/login.html', {'form': form})



@login_required(login_url='/login/')
def account_view(request): 
    

    if request.user.groups.filter(name='manager').exists():
        context = {
        'posts': Post.objects.filter()
        }
        template = 'account_role.html'
    # иначе все остальные (обычные пользователи)
    else:
        context = {
        'posts': Post.objects.filter(author=request.user)
        }
       
        template = 'account.html'

    # сортировка выдачи заказов в обратном порядке (от последнего к первому)    

    return render(request, template, context)

@login_required(login_url='/login/')
def post_new(request):

    context = {}
    context['form'] = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        
        

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.qt = form.cleaned_data['qr']
                     
   
            post.created_date = timezone.now()
            post.save()
            print(post.qr.path, pathlib.Path(__file__).parent.absolute())
            qwee = post.qr.path

            imagess = cv2.imread(qwee)
            
            detector = cv2.QRCodeDetector()

            data, bbox, _ = detector.detectAndDecode(imagess)


            if bbox is not None:
                text_qr = data    
            else:
                text_qr = 'не смог прочитать qr-код с изображения'
            post.textqr = text_qr
            post.save()
            return redirect('/')
    else:
        form = PostForm()
        form.author = request.user
    return render(request, 'add.html', context)



class ProductsDetailView(DetailView):
    model = Post()
    template_name = 'zapros.html'



# изменение данных в бд
def edit(request, id):
    try:
        post = Post.objects.get(id=id)
 
        if request.method == "POST":
            post.textot = request.POST.get("textot")
            post.year_in_school = request.POST.get("year_in_school")
            print(post)
            post.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"post": post})
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>post not found</h2>")
     
# удаление данных из бд
def delete(request, id):
    try:
        post = post.objects.get(id=id)
        post.delete()
        return HttpResponseRedirect("/")
    except post.DoesNotExist:
        return HttpResponseNotFound("<h2>post not found</h2>")