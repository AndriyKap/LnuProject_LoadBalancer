from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
import time
import random
import json
import os
from .models import BellTask
from django.template import loader
import io
from .bell_numbers import bell_recursive
from django.db.models import Q

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
@login_required(login_url="/login")
def bell_numbers(request):
    if request.method == "POST":
        client_id = request.user.id
        value = request.POST.get("value")
        status = 'in progress'
        value = int(value)
        task = BellTask(value=value,user_id_id=client_id,result=0, status=status)
        task.save()

        tasks = BellTask.objects.filter(Q(user_id_id=client_id, status='completed') | Q(user_id_id=client_id, status='in progress'))
        total_tasks = tasks.count()


        if total_tasks <= max_tasks:
            task.result = bell_recursive(value)
            task.status = "completed"
            task.save()

            response_data = {
            'success_message': "Task was done successfully! You can see the result <a href='/list' class='text-primary'>here</a>!"
            }
            return JsonResponse(response_data)
        else:
            task.delete() 
            error_message = f"You have reached the maximum limit of {max_tasks} profiles. Cannot create more tasks."
            return JsonResponse({'error_message': error_message}, status=400)
    return render(request, 'math/bell_numbers.html')


@login_required(login_url="/login")
def list(request):
    client_id = request.user.id
    task = BellTask.objects.filter(user_id_id=client_id, status='completed')
    total_tasks = task.count()
    remaining_tasks = max(0, max_tasks - total_tasks)  
    return render(request, 'math/list.html', {'tasks':task, 'remaining_tasks': remaining_tasks})

@login_required(login_url="/login")
def delete_task(request, id):
    task = get_object_or_404(BellTask, pk=id)
    task.delete()
    return redirect('list')