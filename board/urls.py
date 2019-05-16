from django.urls import path
from .views import document_list, document_detail, document_create, document_update, comment_create, comment_update, comment_delete

app_name = 'board'

urlpatterns = [
    path('update/<int:document_id>/', document_update, name='update'),
    path('comment/create/<int:document_id>/', comment_create, name='comment_create'),
    path('comment/update/<int:comment_id>/', comment_update, name='comment_update'),
    path('comment/delete/<int:comment_id>/', comment_delete, name='comment_delete'),
    path('create/', document_create, name='create'),
    path('detail/<int:document_id>/', document_detail, name='detail'),
    path('', document_list, name='list'),
]