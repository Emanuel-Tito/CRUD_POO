from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # URLs para Empleados
    path('empleados/', views.empleado_list, name='empleado_list'),
    path('empleados/nuevo/', views.empleado_create, name='empleado_create'),
    path('empleados/editar/<int:pk>/', views.empleado_update, name='empleado_update'),
    path('empleados/eliminar/<int:pk>/', views.empleado_delete, name='empleado_delete'),
    
    # URLs para Nóminas
    path('nominas/', views.nomina_list, name='nomina_list'),
    path('nominas/nueva/', views.nomina_create, name='nomina_create'),
    path('nominas/<int:pk>/', views.nomina_detail, name='nomina_detail'),
    path('nominas/eliminar/<int:pk>/', views.nomina_delete, name='nomina_delete'),

    path('signup/', views.signup_view, name='signup'),
    path('signout/', views.signout_view, name='signout'),
    path('signin/', views.signinn, name='signin'),
    
]