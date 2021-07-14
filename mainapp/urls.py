from django.urls import path

from .views import index, del_all_db, top_clients


urlpatterns = [
    path('', index),
    path('del', del_all_db),
    path('top', top_clients)
]
