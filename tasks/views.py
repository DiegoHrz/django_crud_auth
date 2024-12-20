from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
#libreria para guardar una cookie con la info del usuario logeado
from django.contrib.auth import login, logout, authenticate

from django.db import IntegrityError

from .forms import TaskForm
from .models import Task

# Create your views here.
def home(request):
    # return HttpResponse('Hello world')
    # return HttpResponse('<h1>Hello world</h1>')
    # en lugar de retornar un string, es mejor devolver una pagina entera de html
    # RETORNAR UN PAGINA HTML:
    # En la carpeta del proyecto que estes puedes crear una carpeta llamada templates y dentro crea un archivo html 
    # title = 'Hello worldcito'
    return render(request, 'home.html')

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form':UserCreationForm
        })
    else:
        #comprobamos que la contraseña y la confirmacion de la contraseña sean iguales
        if request.POST['password1'] == request.POST['password2']:
            try:
                #guardamos a todo el nuevo usuario creado una variable
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                # lo guardamos en la base de datos
                user.save()
                # esto crea la cookie para guardar la sesion log in
                login(request,user)
                return redirect('tasks')

            #es el error cuando ya existe el user
            except IntegrityError:
                return HttpResponse(render(request,'signup.html',{
                    'form': UserCreationForm,
                    'error': 'Username already exists',
                }))

        return HttpResponse(render(request,'signup.html',{
                    'form': UserCreationForm,
                    'error': "Passwords dont match",
                }))
    
def tasks(request):
    return render(request,'tasks.html')

def sign_out(request):
    logout(request)
    return redirect('home')

def sign_in(request):
    if request.method == 'GET':
        return render(request,'signin.html',{
            'form': AuthenticationForm,
        })
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
            'form': AuthenticationForm,
            'error': 'Username doesnt exist'
        })
        else:
            login(request,user)
            return redirect('/tasks/')


def create_task(request):

    if request.method == 'GET':
        return render(request,'create_tasks.html',{
            'form':TaskForm
        })
    else:
        try:
            #usa el nuevo modelo TaskForm como base
            form = TaskForm(request.POST)
            #para q aun no lo guarde en la db
            new_task = form.save(commit=False)
            #necesita estar asociado con el usuario
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')

        except ValueError :
            return render(request,'create_tasks.html',{
            'form':TaskForm,
            'error':'Please provide valid data'
        })
