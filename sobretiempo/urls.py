from django.urls import path
from .views import (
    SobretiempoCreateView,
    SobretiempoUpdateView,
    SobretiempoDeleteView,
    SobretiempoListView,
)
app_name = 'sobretiempo'
urlpatterns = [
    path('sobretiempo/', SobretiempoListView.as_view(), name='sobretiempo_list'),
    path('sobretiempo/create/', SobretiempoCreateView.as_view(), name='sobretiempo_create'),
    path('sobretiempo/<int:pk>/update/', SobretiempoUpdateView.as_view(), name='sobretiempo_update'),
    path('sobretiempo/<int:pk>/delete/', SobretiempoDeleteView.as_view(), name='sobretiempo_delete'),
]

