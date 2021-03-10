"""readAloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import include
from rest_framework import routers
from django.urls import path
from readAloudapi.views import register_user, login_user, Books


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'books', Books, 'book')

urlpatterns = [
# Requests to http://localhost:8000/books(etc) will be routed to the appropriate function    
    path('', include(router.urls)),
# Requests to http://localhost:8000/register will be routed to the register_user function
    path('register', register_user),
# Requests to http://localhost:8000/login will be routed to the login_user function
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework'))
]
