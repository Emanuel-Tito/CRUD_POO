from django.urls import path
from . import views

app_name = 'prestamos'

urlpatterns = [
    path('prestamo_list', views.prestamo_list, name='prestamo_list'),
    path('nuevo/', views.prestamo_create, name='create'),
    path('<int:pk>/', views.prestamo_detail, name='detail'),
    path('<int:pk>/editar/', views.prestamo_update, name='update'),
    path('<int:pk>/eliminar/', views.prestamo_delete, name='delete'),
]