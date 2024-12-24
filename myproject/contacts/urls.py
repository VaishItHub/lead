from django.urls import path
from . import views

urlpatterns = [
    path('', views.send_messages, name='send_messages'),
]
