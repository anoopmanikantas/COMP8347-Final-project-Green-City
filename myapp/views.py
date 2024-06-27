from django.shortcuts import render

def home(request):
    return render(request, 'm/home.html')

def dashboard(request):
    return render(request, 'm/dashboard.html')

def user_profile(request):
    return render(request, 'm/user_profile.html')

def building_permit_details(request):
    return render(request, 'm/building_permit_details.html')

def status_details(request):
    return render(request, 'm/status.html')

# Add other views as needed for your application
