from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import MyCodeForm
from .models import MyCode
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'mycode/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'mycode/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('mycodes')
            except IntegrityError:
                return render(request, 'mycode/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'mycode/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'mycode/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'mycode/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('mycodes')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createmycode(request):
    if request.method == 'GET':
        return render(request, 'mycode/createmycode.html', {'form':MyCodeForm()})
    else:
        try:
            form = MyCodeForm(request.POST)
            newmycode = form.save(commit=False)
            newmycode.user = request.user
            newmycode.save()
            return redirect('mycodes')
        except ValueError:
            return render(request, 'mycode/createmycode.html', {'form':MyCodeForm(), 'error':'Bad data passed in. Try again.'})


@login_required
def viewmycode(request, mycode_pk):
    mycode = get_object_or_404(MyCode, pk=mycode_pk, user=request.user)
    if request.method == 'GET':
        form = MyCodeForm(instance=mycode)
        return render(request, 'mycode/viewmycode.html', {'mycode':mycode, 'form':form})
    else:
        try:
            form = MyCodeForm(request.POST, instance=mycode)
            form.save()
            return redirect('mycodes')
        except ValueError:
            return render(request, 'mycode/viewmycode.html', {'mycode':mycode, 'form':form, 'error':'Bad info'})

@login_required
def mycodes(request):
    mycode = MyCode.objects.filter(user=request.user)
    return render(request, 'mycode/codes.html', {'mycode':mycode})

@login_required
def deletemycode(request, mycode_pk):
    mycode = get_object_or_404(MyCode, pk=mycode_pk, user=request.user)
    if request.method == 'POST':
        mycode.delete()
        return redirect('mycodes')
