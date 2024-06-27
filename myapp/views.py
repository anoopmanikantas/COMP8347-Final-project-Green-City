from django.shortcuts import render


def home(request):
    return render(request, 'home/home.html')


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def user_profile(request):
    return render(request, 'user_profile/user_profile.html')


def building_permit_details(request):
    return render(request, 'building_permit/building_permit_details.html')


def status_details(request):
    return render(request, 'status/status.html')

