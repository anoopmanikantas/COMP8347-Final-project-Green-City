from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render , redirect
from .forms import BuildingPermitForm, AdminLoginForm, AdminSignupForm, CustomAuthenticationForm, CustomUserCreationForm
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
    if request.method == 'POST':
        form = AdminLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('myapp:adminpage')
    else:
        form = AdminLoginForm()
    return render(request, 'admin/admin_login.html', {'form': form})


def adminsignup(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('myapp:adminlogin')
    else:
        form = AdminSignupForm()
    return render(request, 'admin/admin_signup.html', {'form': form})


def privacy_policy(request):
    return render(request, 'privacy_policy/privacy_policy.html')


def about(request):
    return render(request, 'about/about.html')


def userlogin(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f'You are now logged in as {username}.')
                return redirect('myapp:home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'register/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Account created successfully!')
            return redirect('myapp:login')
        else:
            error_messages = form.errors.as_json()
            return HttpResponse(f'Please correct the error below: {error_messages}')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register/signup.html', {'form': form})


from django.shortcuts import render
from .forms import BuildingPermitForm
from .models import BuildingPermit

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

