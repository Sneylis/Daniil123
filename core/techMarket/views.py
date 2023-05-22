from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import RegisterUserForm, UnitForm, LoginForm
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from .utils import DataMixin
from django.db.models import Sum


# Create your views here.

def about(request):
    return render(request,'techMarket/about.html')
def index(request):
    g = Group.objects.all()
    unit = Unit.objects.all()
    paginator = Paginator(unit, 15)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, 'index.html', {'page_obj': page_obj, 'group': g})

def ShCat(request,cat_id):
    g = Group.objects.all()
    unit = Unit.objects.filter(cat_id=cat_id)
    paginator = Paginator(unit, 15)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, 'index.html', {'page_obj': page_obj, 'group': g})

def ShUnit(request,unit_id):
    g = Group.objects.all()
    l = Like.objects.filter(unit_id=unit_id)
    like = l.count()
    unit = Unit.objects.get(pk=unit_id)
    character = list(unit.character.split(","))
    return render(request, 'techMarket/Unit.html', {'unit': unit, 'group': g,'character':character,'like':like})

class register(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('techMarket:login')

    def get_context_data(self,object_list=None,**kwargs):
        context=super().get_context_data(**kwargs)
        return dict(list(context.items()))

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('login_user:index')
            else:
                form.add_error(None, 'неверный логин или пароль')
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'login.html', {'form': LoginForm()})

def AddUnit(request):
    if request.method == 'POST':
        form = UnitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('techMarket:index')
    else:
        form = UnitForm()
        return render(request, 'techMarket/addUnit.html', {'form': form})

class updunit(UpdateView):
    model = Unit
    template_name = 'techMarket/updUnit.html'
    success_url = '/'

    fields = ['title', 'about', 'character', 'price', 'photo','cat']

def delunit(request,unit_id):
    if request.user.has_perm('unit.add_Unit'):
        unit = Unit.objects.get(pk=unit_id)
        try:
            unit.delete()
            return redirect('techMarket:index')
        except:
            message="delete wasn't successful"
        return render(request,'index.html',{'message':message})
    else:
        return reverse_lazy('techMarket:index')

@login_required(login_url='techMarket:login')
def addBucket(request,unit_id):
    unit = Unit.objects.get(pk=unit_id)
    user = request.user
    try:
        b = Backet.objects.get(user=user,unit=unit)
        if b:
            b.l += 1
        b.save()
        message = f'{b.unit}добавлен в корзину в колличестве{b.l}'
        return redirect('techMarket:index')
    except:
        b = Backet(user=user,unit=unit,l=1)
        b.save()
        message = 'успешно добавлен товар'
        return redirect('techMarket:index')

@login_required(login_url='techMarket:login')
def ShBucket(request):
    user = request.user
    b = Backet.objects.filter(user=user)
    price = 0
    for i in b:
        if i.l > 1:
            price = price + int(i.unit.price) * i.l
        else:
            price = price + int(i.unit.price)

    return render(request,'bucket.html',{'unit':b,'price':price})

def delBucket(request,bucket_id):
    b = Backet.objects.get(pk=bucket_id)
    if b.l > 1:
        b.l = b.l - 1
        b.save()
        return redirect('techMarket:ShBucket')
    else:
        b.delete()
        return redirect('techMarket:ShBucket')



@login_required(login_url='techMarket:login')
def addLike(request,unit_id):
    try:
        l = Like.objects.get(unit_id=unit_id,user=request.user,like=True)
        l.delete()
        return redirect(f"/unit/{unit_id}")
    except:
        l = Like(unit_id=unit_id,user=request.user,like=True)
        l.save()
        return redirect(f"/unit/{unit_id}")


@login_required(login_url='techMarket:login')
def addComment(request,unit_id):
    b = Unit.objects.get(pk=unit_id)
    com = request.POST['comment']
    user_comment = comment(unit=b,text=com,user=request.user)
    user_comment.save()
    return redirect(f"/unit/{unit_id}")





