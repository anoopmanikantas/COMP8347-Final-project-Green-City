from django.shortcuts import render , redirect
from .forms import BuildingPermitForm
from .models import BuildingPermit


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


def adminlogin(request):
    return render(request, 'admin/admin_login.html')


def adminsignup(request):
    return render(request, 'admin/admin_signup.html')


def privacy_policy(request):
    return render(request, 'privacy_policy/privacy_policy.html')


def about(request):
    return render(request, 'about/about.html')


def login(request):
    return render(request, 'register/login.html')


def signup(request):
    return render(request, 'register/signup.html')


def calculate_trees(area, floors):
    area_map = {
        '0-0.3': 1,
        '0.3-0.5': 2,
        '0.5-0.7': 3,
        '0.7+': 4,
    }
    floors_map = {
        '1-3': 1,
        '4-6': 2,
        '7+': 3,
    }
    return area_map[area] * floors_map[floors]

def building_permit_application(request):
    if request.method == 'POST':
        form = BuildingPermitForm(request.POST, request.FILES)
        if form.is_valid():
            permit = form.save(commit=False)
            permit.trees_required = calculate_trees(permit.area, permit.floors)
            permit.save()
            return render(request, 'building_permit/result.html', {'trees_required': permit.trees_required})
    else:
        form = BuildingPermitForm()
    return render(request, 'building_permit/apply.html', {'form': form})
