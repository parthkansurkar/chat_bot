from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view),
    path('chat/', views.chatbot_api),
]