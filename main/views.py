from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Task, Renter
from .forms import TaskForm


# Create your views here.
def index(request):
    tasks=Task.objects.all()
    return render(request, 'main/index.html', {'title':'Главная страница', 'tasks':tasks})


def about(request):
    return render(request, 'main/about.html')


def add(request):
    error=""
    if request.method=='POST':
        form=TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error='Форма была неверной'
    form=TaskForm()
    context={
        'form': form,
        'error': error
    }
    return render(request, 'main/add.html', context)




