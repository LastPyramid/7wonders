from django.urls import path
from .views import LoginAPIView, RegisterAPIView, LogoutAPIView
from . import views

urlpatterns = [
    path('create', views.create),
    path('send', views.send), # REMOVE THIS I THINK
    path('start', views.start),
    path('init', views.csrf_init),
    path('lobbies', views.lobbies),
    path('login', LoginAPIView.as_view()),
    path('register', RegisterAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('fetchgames', views.lobbies), # change name?
]