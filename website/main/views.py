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
import threading
import os
from .models import BellTask
from django.http import HttpResponse
from django.template import loader
import io
from django.shortcuts import get_object_or_404, redirect
import time
from .bell_numbers import bell_recursive
from concurrent.futures import ThreadPoolExecutor
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F
from .bell_numbers import TaskCancelledException 

# Create your views here.

@login_required(login_url="/login")
def home(request):
    return render(request, 'main/home.html')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


executor = ThreadPoolExecutor(max_workers=2)
max_tasks = 10
@csrf_exempt
@login_required(login_url="/login")
def bell_numbers(request):
    if request.method == "POST":
        client_id = request.user.id
        
        tasks = BellTask.objects.filter(Q(user_id_id=client_id, status='completed') | Q(user_id_id=client_id, status='in progress'))
        total_tasks = tasks.count()

        if total_tasks < max_tasks:
            value = request.POST.get("value")
            status = 'in progress'
            value = int(value)
            task = BellTask(value=value, user_id_id=client_id, result=0, status=status, progress=0)
            task.save()

            executor.submit(run_background_task, task.id, value)

            response_data = {
                'task_id': task.id,
                'success_message': "Task started successfully! You can check the result later."
            }
            return JsonResponse(response_data)
        else:
            error_message = f"You have reached the maximum limit of {max_tasks} profiles. Cannot create more tasks."
            return JsonResponse({'error_message': error_message}, status=400)
    return render(request, 'math/bell_numbers.html')


def update_progress(task_id):
    task = BellTask.objects.get(pk=task_id)
    i = 0
    while True:
        time.sleep(1)
        task.refresh_from_db()
        if task.status == "cancelled":
            print("cancelled on update")
            task.result = -1
            task.save()
            break
        if task.status == "completed":
            break

        i += 1
        i %= 100

        BellTask.objects.filter(pk=task_id).update(progress=i)


def run_background_task(task_id, value):  
    task = BellTask.objects.get(pk=task_id)
    task.status = "in progress"
    task.save()

    threading.Thread(target=update_progress, args=(task_id,)).start()

    try:
        task.result = bell_recursive(value, task_id)
        task.status = "completed"
        task.progress = 100
        task.save()
        return task.id
    except TaskCancelledException as e:
        print(f"An error occurred: {e}")
        task.refresh_from_db()
        if task.status == "cancelled":
            print("im cancelled in run_back")
            task.result = -1
            task.save()
            return task.id
    

@login_required(login_url="/login")
def get_progress(request, task_id):
    task = get_object_or_404(BellTask, pk=task_id)
    return JsonResponse({'progress': task.progress})


@login_required(login_url="/login")
@csrf_exempt
def cancel_task(request, task_id):
    task = get_object_or_404(BellTask, pk=task_id)

    task.status = 'cancelled'
    task.save()

    response_data = {
        'success_message': 'Task cancelled successfully!',
    }
    return JsonResponse(response_data)

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