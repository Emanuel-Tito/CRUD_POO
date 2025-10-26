from django.urls import path
from .views import (
    EmpleadoListView, EmpleadoCreateView, EmpleadoUpdateView, EmpleadoDeleteView,
    NominaListView, NominaCreateView, NominaDetailView, NominaDeleteView,
    HomeView, SignupView, SignoutView, SigninView
)


app_name='nomina'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('empleados/', EmpleadoListView.as_view(), name='empleado_list'),
    path('empleados/create/', EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleados/<int:pk>/update/', EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleados/<int:pk>/delete/', EmpleadoDeleteView.as_view(), name='empleado_delete'),

    path('nominas/', NominaListView.as_view(), name='nomina_list'),
    path('nominas/create/', NominaCreateView.as_view(), name='nomina_create'),
    path('nominas/<int:pk>/', NominaDetailView.as_view(), name='nomina_detail'),
    path('nominas/<int:pk>/delete/', NominaDeleteView.as_view(), name='nomina_delete'),

    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('signout/', SignoutView.as_view(), name='signout'),
]
