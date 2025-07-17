from django.urls import path
from . import views

app_name = 'managers'

urlpatterns = [
    # Set manager_view as the default view when accessing managers page
    path('managerhome/', views.manager_home, name='manager_home'),
    path('revenue_gen/', views.revenue_gen, name='revenue_gen'),
    path('hourusage/', views.hour_of_usage, name='hour_of_usage'),
    path('vehicles_fixed_most/', views.vehicles_fixed_most, name='vehicles_fixed_most'),
    path('age_group/', views.age_group, name='age_group'),
]
