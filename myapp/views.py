from django.shortcuts import render


def home(request):
    return render(request, 'home/home.html')


def dashboard(request):
    return render(request, 'home/dashboard/dashboard.html')


def user_profile(request):
    return render(request, 'user_profile/user_profile.html')


def building_permit_details(request):
    return render(request, 'building_permit/building_permit_details.html')


def status_details(request):
    return render(request, 'status/status.html')

def adminpage(request):
    return render(request, 'admin/admin_page.html')

def privacy_policy(request):
    return render(request, 'privacy_policy/privacy_policy.html')


def about(request):
    return render(request, 'about/about.html')

def login(request):
    return render(request, 'register/login.html')

def signup(request):
    return render(request, 'register/signup.html')