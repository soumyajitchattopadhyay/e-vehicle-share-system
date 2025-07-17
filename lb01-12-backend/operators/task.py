# operators/tasks.py
from celery import shared_task
import time
from .models import Vehicle

@shared_task
def charge_vehicle_task(vehicle_id):
    try:
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)

        # Set to 'charging' if the current status is 'depleted'
        if vehicle.status.lower() == 'depleted':
            vehicle.status = 'charging'
            vehicle.save(update_fields=['status'])

        # Simulate the charging process
        while vehicle.battery_level < 100:
            vehicle.battery_level = min(vehicle.battery_level + 5, 100)  # Ensure it doesn't exceed 100%
            vehicle.save(update_fields=['battery_level'])
            time.sleep(5)  # Adjust timing as needed

        # Set status to 'available' when fully charged
        vehicle.status = 'available'
        vehicle.save(update_fields=['status', 'battery_level'])

    except Vehicle.DoesNotExist:
        print(f"Vehicle with ID {vehicle_id} does not exist.")
    except Exception as e:
        print(f"An error occurred while charging the vehicle {vehicle_id}: {e}")

@shared_task  # Ensures this function is registered as a Celery task
def repair_vehicle_task(vehicle_id):
    try:
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
        vehicle.status = 'in_repair'
        vehicle.save(update_fields=['status'])

        # Simulate repair delay
        time.sleep(10)  # Adjust to a realistic repair time

        vehicle.status = 'available'
        vehicle.save(update_fields=['status'])
    except Vehicle.DoesNotExist:
        print(f"Vehicle with ID {vehicle_id} does not exist.")
