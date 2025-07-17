from django.urls import path,include
from . import views

urlpatterns = [
    # Set login_view as the default view when accessing the root URL
    path('', views.login_user, name="home"),

    # Other paths
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    
    # Vehicle rent page
    path('vehiclerent/', views.vehicle_rent_view, name='vehiclerent'),
    
    # Location page
    path('location/', views.location_view, name='location'),
    
    path('payment-option/', views.payment_option_view, name='payment_option'),
    path('add_money/', views.add_money, name='add_money'),
    path('store-trip/', views.store_trip, name='store_trip'),
    # path('receipt/', views.receipt, name='receipt'),
    path('managers/', include('managers.urls')),
    path('receipt/<str:price>/', views.receipt, name='receipt'),
    path('get-available-vehicles/<str:vehicle_type>/', views.get_available_vehicles, name='get_available_vehicles'),

]
