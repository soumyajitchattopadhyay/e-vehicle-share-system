from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import trip, Profile

@csrf_exempt
def store_trip(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            distance = data['distance']
            price = float(data['price'])
            time = data['time']
            latitude = data['latitude']
            longitude = data['longitude']
            
            trip.objects.create(
                distance=distance,
                price=price,
                time=time,
                latitude=latitude,
                longitude=longitude
            )
            
            user = request.user.profile
            if user.balance >= price:
                user.balance -= price
                user.save()
            else:
                return JsonResponse({'success': False, 'error': 'Insufficient balance'})

            # Return a success response
            return JsonResponse({'success': True})
        
        except (KeyError, ValueError) as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)

# @login_required
@csrf_exempt
def add_money(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = float(data.get('balance', 0))
        user = request.user.profile 
        
        if amount > 0:
            user.balance += amount
            user.save()
            return JsonResponse({"success": True,'new_balance': user.balance})
        else:   
            return JsonResponse({"success": False, "error": "Invalid amount"})
    return JsonResponse({"success": False, "error": "Invalid request"})

def receipt(request):
    price = request.GET.get('price') 
    if price is None:

        return render(request, 'error.html', {'message': 'Price not provided.'})

    return render(request, 'loginpage/receipt.html', {'price': price})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       # identity = request.POST['identity']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            user_role = user.profile.identity 
            print(user_role)
            login(request, user)
            if user_role == 'manager':
                # manager login successful
                return redirect('managers:manager_home')
            
            elif user_role == 'operator':
                # manager login successful
                return redirect('operators:operator_dashboard')

            elif user_role == 'user':
                # Customer login successful
                return redirect('vehiclerent')  # Redirect to the vehicle rent page
        else:
            # Invalid credentials
            messages.success(request,("There was an error, try again!"))
            return redirect('login')
        
    return render(request, 'loginpage/login.html')

def logout_user(request):
    logout(request)
    messages.success(request,("You have been logout!!"))
    return redirect('login')

def location_view(request):
    vehicle_id = request.GET.get('vehicle', 'Unknown')
    return render(request, 'loginpage/location.html', {'vehicle_id': vehicle_id})

# @login_required
def vehicle_rent_view(request):

    return render(request, 'loginpage/vehiclerent.html')

@csrf_exempt
def payment_option_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        payment_amount = data.get("amount", 0)
        try:
            if request.user.profile.balance >= payment_amount:
                request.user.profile.balance -= payment_amount
                request.user.profile.save()
                return JsonResponse({"success": True, "balance": request.user.profile.balance})
            else:
                return JsonResponse({"success": False, "error": "Insufficient balance"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return render(request, 'loginpage/payment_option.html')

def signup_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid() and form.email != user.email:
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for '+ user)
            return redirect('login')
    context = {'form':form}
    return render(request, 'loginpage/signup.html',context)

def get_available_vehicles(request, vehicle_type):
    vehicles = Vehicle.objects.filter(vehicle_type=vehicle_type, is_available=True).values('id', 'name') ## Vehicle = the model of the databse having the vehicle information
    return JsonResponse(list(vehicles), safe=False)

