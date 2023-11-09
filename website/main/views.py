from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
import time
import random
import json
import os
from .models import BellTask
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
from django.shortcuts import get_object_or_404, redirect
import time
from .bell_numbers import bell_recursive

# Create your views here.

@login_required(login_url="/login")
def home(request):
    return render(request, 'main/home.html')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


max_tasks = 10
def bell_numbers(request):
    if request.method == "POST":
        client_id = request.user.id
        tasks = BellTask.objects.filter(user_id_id=client_id, status='completed')
        total_tasks = tasks.count()

        if total_tasks < max_tasks:
            value = request.POST.get("value")
            status = 'in progress'
            value = int(value)
            task = BellTask(value=value,user_id_id=client_id,result=0, status=status)
            task.save()
            task.result = bell_recursive(value)
            task.status = "completed"
            task.save()

            response_data = {
            'success_message': "Task was done successfully! You can see the result <a href='/list' class='text-primary'>here</a>!"
            }
            return JsonResponse(response_data)
        else:
            error_message = f"You have reached the maximum limit of {max_tasks} profiles. Cannot create more tasks."
            return JsonResponse({'error_message': error_message}, status=400)
    return render(request, 'pdf/bell_numbers.html')


def list(request):
    client_id = request.user.id
    task = BellTask.objects.filter(user_id_id=client_id, status='completed')
    total_tasks = task.count()
    remaining_tasks = max(0, max_tasks - total_tasks)  
    return render(request, 'pdf/list.html', {'tasks':task, 'remaining_tasks': remaining_tasks})

def delete_task(request, id):
    task = get_object_or_404(BellTask, pk=id)
    task.delete()
    return redirect('list')