from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.CustomRegisterView),
    path('activate/', views.AuthenticateView)
]