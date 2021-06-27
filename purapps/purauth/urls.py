from django.urls import path
from . import views

# app_name = 'inscripts'

urlpatterns = [
    # path('inscription/', views.inscriptions.as_view(), name='inscription'),
    # path('inscription/', views.inscriptions),
    path("registration/inscript", views.inscript),
]
