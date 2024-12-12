# csv_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    # path('data/', views.get_data, name='get_data'),
]
