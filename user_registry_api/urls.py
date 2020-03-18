"""user_registry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from user_registry_api.rest import add_new_user, handle_existing_user, get_users

app_name = 'user_registry_api'
urlpatterns = [
    path('add_new_user', add_new_user, name='add_new_user'),
    path('user/<int:user_id>', handle_existing_user, name='handle_existing_user'),
    path('get_users', get_users, name='get_users')
]
