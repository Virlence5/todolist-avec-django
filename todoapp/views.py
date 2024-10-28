from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Todo
from django.contrib.auth.decorators import login_required


@login_required
def home(request) :

    if request.method == "POST" :
        task = request.POST.get("task")
        new_todo = Todo(user = request.user, todo_name = task)
        new_todo.save()

    all_todos = Todo.objects.filter(user = request.user)
    context = {
        'todos' : all_todos
    }

    return render(request, "todoapp/todo.html", context)



def register(request) :

    if request.user.is_authanticated :
        return redirect("home")

    if request.method == "POST" :
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if len(password) < 5 :
            messages.error(request,"Password most be at least 5 characters.")
            return redirect("register")

        get_all_user_by_username = User.objects.filter(username = username)
        if get_all_user_by_username :
            messages.error(request,"Error, this username already exist, use another.")
            return redirect("register")

        get_all_user_by_email = User.objects.filter(email = email)
        if get_all_user_by_email :
            messages.error(request,"Error, this email already exists, use another.")
            return redirect("register")

        new_user = User.objects.create_user(username = username, email = email, password = password)
        new_user.save()
        return redirect("login")


    return render(request,"todoapp/register.html", {})



def loginPage(request) :

    if request.method == "POST" :
        username = request.POST.get("uname")
        password = request.POST.get("pass")

        validate_user = authenticate(username = username, password = password)
        if validate_user is not None :
            login(request, validate_user)
            return redirect("home-page")
        else :
            messages.error(request,"Error, wrong user details or this user does not exists.")
            messages.success(request, "User successfully created, login now")
            return redirect("login")

    return render(request,"todoapp/login.html", {})



def logoutView(request) :

    logout(request)
    return redirect("login")



@login_required
def deleteTask(request, name) :

    get_todo = Todo.objects.get(user=request.user, todo_name = name)
    get_todo.delete()
    return redirect("home-page")



@login_required
def update(request,name) :

    get_todo = Todo.objects.get(user=request.user, todo_name = name)
    get_todo.status = True
    get_todo.save()
    return redirect("home-page")

