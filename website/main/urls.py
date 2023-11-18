from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name ='home'),
    path('sign-up', views.sign_up, name ='sign_up'),
    path('bell-number/', views.bell_numbers, name='bell_number'),
    path('list', views.list,name="list"),
    path('delete/<int:id>/', views.delete_task, name='delete_task'),
    path('get_progress/<int:task_id>/', views.get_progress, name='get_progress'),
    path('cancel_task/<int:task_id>/', views.cancel_task, name='cancel_task'),
]