# operators/views.py

from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from .models import Vehicle, Location
import json
from .task import charge_vehicle_task, repair_vehicle_task  # Ensure file name matches
from django.shortcuts import render


# View to track vehicle details and check if it matches a station's coordinates
def track_vehicle(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)

        # Use station name if location_station is set, otherwise fallback to coordinates
        location_name = vehicle.location_station.name if vehicle.location_station else f"Latitude {vehicle.latitude}, Longitude {vehicle.longitude}"

        # Prepare the response data
        data = {
            "vehicle_id": vehicle.vehicle_id,
            "vtype": vehicle.vtype,
            "battery_level": vehicle.battery_level,
            "status": vehicle.status,
            "last_updated": vehicle.last_updated.strftime("%Y-%m-%d %H:%M:%S"),
            "location": location_name,
        }

        print(f"Debug Info - Vehicle ID: {vehicle.vehicle_id}, Location: {data['location']}")  # Print debug info

        return JsonResponse(data)
    except Vehicle.DoesNotExist:
        return JsonResponse({"error": "Vehicle not found"}, status=404)
    
def get_vehicles(request):
    vehicles = Vehicle.objects.all().values('vehicle_id', 'battery_level', 'status', 'location_station__name')
    vehicle_data = [
        {
            'vehicle_id': v['vehicle_id'],
            'battery_level': v['battery_level'],
            'status': v['status'],
            'in_station': v['location_station__name'] is not None,
            'station_name': v['location_station__name']
        }
        for v in vehicles
    ]
    return JsonResponse(vehicle_data, safe=False)

# Dashboard view
def operator_dashboard(request):
    return render(request, 'operators/OperatorFront.html')

# CSRF-exempt decorator added to allow AJAX POST requests from the front end
@csrf_exempt
def charge_vehicle(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
        
        if vehicle.status.lower() == 'depleted':
            charge_vehicle_task.delay(vehicle_id)  # Trigger async task
            return JsonResponse({"message": f"Vehicle {vehicle_id} is now charging."})
        else:
            return JsonResponse({"message": "Vehicle is not depleted and cannot be charged."})
    except Vehicle.DoesNotExist:
        return JsonResponse({"error": "Vehicle not found"}, status=404)

@csrf_exempt
def repair_vehicle(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)

        # Initiate the repair task asynchronously
        repair_vehicle_task.delay(vehicle_id)

        # Respond immediately to indicate repair has started
        return JsonResponse({"message": f"Repair started for vehicle {vehicle_id}"})
    except Vehicle.DoesNotExist:
        return JsonResponse({"error": "Vehicle not found"}, status=404)
    
def get_vehicle_battery_status(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
        return JsonResponse({
            'vehicle_id': vehicle.vehicle_id,
            'battery_level': vehicle.battery_level,
            'status': vehicle.status
        })
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)
    
@csrf_exempt
def move_vehicle(request, vehicle_id):
    if request.method == 'POST':
        try:
            vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
        except Vehicle.DoesNotExist:
            return JsonResponse({"error": "Vehicle not found"}, status=404)

        # Parse the JSON body for the station data
        data = json.loads(request.body)
        station_name = data.get('station')  # Extract station from JSON data

        if not station_name:
            return JsonResponse({"error": "Station not provided"}, status=400)

        # Retrieve or create the station and associate it with the vehicle
        station, created = Location.objects.get_or_create(name=station_name)
        vehicle.location_station = station
        vehicle.status = 'moving'  # Assuming the move action implies the vehicle is "moving"
        vehicle.save()

        return JsonResponse({"message": f"Vehicle {vehicle_id} successfully moved to {station_name}!"})
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
