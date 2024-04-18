from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('images_result/', views.images_result, name='images_result'),
    path('login/', views.login_view, name='login'),
]
