from django.urls import path
from .views import (
    PrestamoListView,
    PrestamoCreateView,
    PrestamoDetailView,
    PrestamoUpdateView,
    PrestamoDeleteView,
)

app_name = 'prestamos'

urlpatterns = [
    path('', PrestamoListView.as_view(), name='prestamo_list'),
    path('create/', PrestamoCreateView.as_view(), name='prestamo_create'),
    path('<int:pk>/', PrestamoDetailView.as_view(), name='prestamo_detail'),
    path('<int:pk>/update/', PrestamoUpdateView.as_view(), name='prestamo_update'),
    path('<int:pk>/delete/', PrestamoDeleteView.as_view(), name='prestamo_delete'),
]
