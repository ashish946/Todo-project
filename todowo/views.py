from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import Todo
from .forms import TodoForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request,'home.html')

def signupuser(request):
    if request.method=='GET':
        return render(request,'signup.html')
    else:
        if request.POST['password'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],request.POST['emailid'],request.POST['password'])
                user.save()
                login(request,user)
                return redirect('currenttodo')
            except IntegrityError:
                return render(request,'signup.html',{'error':'Username is already taken. Please try something else.'})
        else:
            return render(request,'signup.html',{'error':'Password did not match please re-enter'})

def loginuser(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('currenttodo')
        else:
            return render(request,'login.html',{'error':'Invalid Credentials...'})

@login_required
def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')


@login_required
def currenttodo(request):
    todos=Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'currenttodo.html',{'todos':todos})

@login_required
def completed(request):
    todos=Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'completed.html',{'todos':todos})

@login_required
def createtodos(request):
    if request.method=='GET':
        return render(request,'create.html',{'form':TodoForm()})
    else:
        try:
            form=TodoForm(request.POST)
            todo=form.save(commit=False)
            todo.user=request.user
            todo.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request,'create.html',{'form':TodoForm(),'error':'Bad data entered'})

@login_required
def viewtodo(request, todo_pk):
    todo=get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method=='GET':
        form=TodoForm(instance=todo)
        return render(request, 'viewtodo.html',{'todo':todo,'form':form})
    else:
        try:
            form=TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodo')

        except ValueError:
            return render(request,'viewtodo.html',{'todo':todo,'form':form,'error':'Bad data Entered. Try Again'})

@login_required
def completetodo(request,todo_pk):
    todo=get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method=='POST':
        todo.datecompleted=timezone.now()
        todo.save()
        return redirect('currenttodo')

@login_required
def deletetodo(request,todo_pk):
    todo=get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method=='POST':
        todo.delete()
        return redirect('currenttodo')

