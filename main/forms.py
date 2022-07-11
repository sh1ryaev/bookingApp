
from .models import Task, Renter, RentObject
from django.forms import ModelForm, TextInput, Textarea, Form, CharField, DateTimeField
from django.db import models

class TaskForm(ModelForm):
    class Meta:
        model= Task
        fields= ["title","task"]
        widgets={
            "title": TextInput(attrs={
            'class':'form-control mt-4',
            'placeholder':'Введите название'
            }),
            "task": Textarea(attrs={
                'class': 'form-control mt-4',
                'placeholder': 'Введите описание'
            }),
            }


class TaskForm(ModelForm):
    class Meta:
        model= Task
        fields= ["title","task"]
        widgets={
            "title": TextInput(attrs={
            'class':'form-control mt-4',
            'placeholder':'Введите название'
            }),
            "task": Textarea(attrs={
                'class': 'form-control mt-4',
                'placeholder': 'Введите описание'
            }),
            }





