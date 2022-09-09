from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_list, name='main'),
    path('add_account', views.add_account, name='add_account'),
]