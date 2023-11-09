from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name ='home'),
    path('sign-up', views.sign_up, name ='sign_up'),
    path('bell-number/', views.bell_numbers, name='bell_number'),
    path('list', views.list,name="list"),
    path('delete/<int:id>/', views.delete_task, name='delete_task')
]