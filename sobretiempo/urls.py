from django.urls import path
from . import views

app_name = 'sobretiempo'

urlpatterns = [
    path('', views.sobretiempo_list, name='list'),
    path('nuevo/', views.sobretiempo_create, name='create'),
    path('<int:pk>/editar/', views.sobretiempo_update, name='update'),
    path('<int:pk>/eliminar/', views.sobretiempo_delete, name='delete'),
]