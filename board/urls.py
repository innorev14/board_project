from django.urls import path
from .views import document_list, document_detail

app_name = 'board'

urlpatterns = [
    path('detail/<int:document_id>/', document_detail, name='detail'),
    path('', document_list, name='list'),
]