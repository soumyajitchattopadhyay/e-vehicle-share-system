# operators/urls.py
from django.urls import path
from . import views

app_name = 'operators'  # Specify the app name for this URL configuration module

urlpatterns = [
    path('track_vehicle/<str:vehicle_id>/', views.track_vehicle, name='track_vehicle'),
    path('charge_vehicle/<str:vehicle_id>/', views.charge_vehicle, name='charge_vehicle'),
    path('repair_vehicle/<str:vehicle_id>/', views.repair_vehicle, name='repair_vehicle'),  # Keep only one
    path('move_vehicle/<str:vehicle_id>/', views.move_vehicle, name='move_vehicle'),
    path('dashboard/', views.operator_dashboard, name='operator_dashboard'),
    path('get_vehicles/', views.get_vehicles, name='get_vehicles'),
    path('api/vehicle/<str:vehicle_id>/status/', views.get_vehicle_battery_status, name='vehicle_battery_status'),
]
