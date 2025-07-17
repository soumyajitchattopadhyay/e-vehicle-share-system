from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from operators.models import Vehicle

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('user', 'User'),
        ('manager', 'Manager'),
        ('operator', 'Operator'),
    ]
    identity = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    date_of_birth = models.DateField(null=True)
    balance= models.FloatField(default=0.0,validators=[MinValueValidator(0)])

    def __str__(self):
        return self.username

class trip(models.Model):
    Vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="trip", null=True)
    distance = models.FloatField(validators=[MinValueValidator(0)])
    price = models.FloatField(validators=[MinValueValidator(0)])
    time = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def vehicle_id(self):
        return self.Vehicle.vehicle_id
    
    @property
    def vtype(self):
        return self.Vehicle.vtype
    
    @property
    def latitude(self):
        return self.Vehicle.latitude

    @property
    def longitude(self):
        return self.Vehicle.longitude
    
    def __str__(self):
        return f"Trip - {self.distance} km - {self.price} $"
    
class incidents(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    trip = models.ForeignKey(trip,on_delete=models.CASCADE, related_name="incident")
    description=models.TextField(max_length=20,default="")

    @property
    def latitude(self):
        # Directly access the latitude from the related Trip
        return self.trip.latitude

    @property
    def longitude(self):
        # Directly access the longitude from the related Trip
        return self.trip.longitude
    
    @property
    def vehicle_id(self):
        return self.trip.vehicle_id
    
    @property
    def vtype(self):
        return self.trip.vtype

    def __str__(self):
        return f"Incident {self.id} related to {self.trip}"
