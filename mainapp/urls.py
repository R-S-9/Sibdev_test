from django.urls import path

from .views import index,delet_all_db


urlpatterns = [
    path('', index),
    path('delet', delet_all_db),
]
