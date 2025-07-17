import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg,Sum,Count,Q, Case, When,Value, F
from operators.models import Vehicle,Location
from loginpage.models import trip,incidents,Profile
from django.http import HttpResponse
from datetime import datetime
from django.db.models.functions import ExtractMonth, ExtractHour

def rev_cal():
    monthly_revenue = trip.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(total_price=Sum('price')).order_by('month')
    month_labels = [datetime(2024, i, 1).strftime('%B') for i in range(1, 13)]
    monthly_data = {month['month']: month['total_price'] for month in monthly_revenue}
    monthly_prices = [monthly_data.get(i, 0) for i in range(1, 13)]
    months = [month_labels[i-1] for i in range(1, 13)]
    prices = [monthly_prices[i-1] for i in range(1, 13)]
    return months,prices

def time_usage():
    time_of_day_data = trip.objects.annotate(hour=ExtractHour('created_at')).annotate(time_of_day=Case(When(hour__lt=12, then=Value('Morning')), When(hour__gte=12, hour__lt=18, then=Value('Afternoon')), When(hour__gte=18, hour__lt=21, then=Value('Evening')),When(hour__gte=21, then=Value('Night')), default=Value('Unknown'))).values('time_of_day').annotate(total=Count('id')).order_by('time_of_day')
    time_labels = [entry['time_of_day'] for entry in time_of_day_data]
    time_counts = [entry['total'] for entry in time_of_day_data] 
    return time_labels,time_counts

def vehicle_fixes_chart():
    vehicles = Vehicle.objects.all().values('vehicle_id', 'number_of_fixes')
    vehicle_ids = [vehicle['vehicle_id'] for vehicle in vehicles]
    fixes_counts = [vehicle['number_of_fixes'] for vehicle in vehicles]
    return vehicle_ids,fixes_counts

def age_group_chart():
    current_year = datetime.now().year
    age_groups = Profile.objects.annotate(
        age=current_year - F('date_of_birth__year'),
        age_group=Case(
            When(age__gte=10, age__lt=27, then=Value('Gen Z')),  # 1997-2012
            When(age__gte=27, age__lt=43, then=Value('Millennials')),  # 1981-1996
            When(age__gte=43, age__lt=59, then=Value('Gen X')),  # 1965-1980
            default=Value('Other')
        )
    ).values('age_group').annotate(count=Count('id')).order_by('age_group')
    groups = [group['age_group'] for group in age_groups]
    counts = [group['count'] for group in age_groups]
    return groups,counts

@login_required
def manager_home(request):    
    full_name = request.user.username
    months,prices = rev_cal()
    time_labels,time_counts = time_usage()
    vehicle_ids,fixes_counts = vehicle_fixes_chart()
    groups,counts = age_group_chart()
    
    context = {
        'usage_data': json.dumps(prices),
        'label':json.dumps(months),
        'time_counts': json.dumps(time_counts),
        'time_labels':json.dumps(time_labels),
        'vehicle_ids':json.dumps(vehicle_ids),
        'fixes_counts':json.dumps(fixes_counts),
        'counts':json.dumps(counts),
        'groups':json.dumps(groups),
        'full_name': full_name
    }
    return render(request, 'managerHomePage.html', context)

@login_required
def revenue_gen(request):
    monthly_revenue = trip.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(total_price=Sum('price')).order_by('month')
    months,prices = rev_cal()
    full_name = request.user.username

    context = {
        'usage_data': json.dumps(prices),
        'label':json.dumps(months),
        'full_name': full_name
    }
    return render(request, 'revenue_Gen.html', context)

@login_required
def hour_of_usage(request):
    time_labels,time_counts = time_usage()
    full_name = request.user.username
    context = {
        'time_counts': json.dumps(time_counts),
        'time_labels':json.dumps(time_labels),
        'full_name': full_name
    }
    return render(request, 'hour_of_usage.html', context)

@login_required
def vehicles_fixed_most(request):
    full_name = request.user.username
    vehicle_ids,fixes_counts = vehicle_fixes_chart()
    context = {
        'vehicle_ids': json.dumps(vehicle_ids),
        'fixes_counts':json.dumps(fixes_counts),
        'full_name': full_name

    }
    return render(request, 'vehicles_fixed_most.html',context) 

@login_required
def age_group(request):
    groups,counts = age_group_chart()
    full_name = request.user.username
    context = {
        'groups':json.dumps(groups),
        'counts':json.dumps(counts),
        'full_name': full_name
    }
    return render(request, 'age_group.html',context) 