# operators/models.py

from django.db import models
from django.utils import timezone

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('E-Bike', 'E-Bike'),
        ('Scooter', 'Scooter'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('depleted', 'Depleted'),
        ('charging', 'Charging'),
        ('in_repair', 'In Repair'),
        ('moving', 'Moving'),
    ]

    vehicle_id = models.CharField(max_length=100, unique=True)  # Added unique=True to prevent duplicate IDs
    vtype = models.CharField(max_length=50, choices=VEHICLE_TYPES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    battery_level = models.PositiveIntegerField(default=100)  # Set default battery level to 100%
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')  # Set default status to 'available'
    last_updated = models.DateTimeField(auto_now=True)  # Auto-update to current time on each save
    number_of_fixes = models.IntegerField(default=0)
    location_station = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle_id} - {self.vtype}"