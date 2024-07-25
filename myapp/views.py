from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BuildingPermitForm, SearchForm, FilterForm, AdminLoginForm, AdminSignupForm, \
    CustomAuthenticationForm, \
    CustomUserCreationForm, ContactForm
from .models import BuildingPermit, CustomUser
from .respository import Repository

repository = Repository()


def home(request):
    building_permits_count = repository.get_building_permits()
    form = SearchForm(request.GET or None)
    results = []
    message = ""
    if form.is_valid():
        query = form.cleaned_data['query']
        # 1. Search for the name first if it exists.
        building_permits = repository.get_building_permits(query=query, user_id=request.user.id)

        if len(building_permits) != 0:
            results = building_permits
        else:
            message = "No permits found"
        # 3. else maintain empty result set and display the same.
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(
            request,
            'home/applications/applications_card.html',
            {
                "form": form,
                "results": results,
                'result_count': len(results),
                'message': message,
            }
        )

    return render(
        request,
        'home/home.html',
        {
            "permits": building_permits_count,
            "form": form,
            'results': results,
            'result_count': len(results),
            'message': message,
        }
    )


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
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('myapp:admin_dashboard')
            else:
                messages.error(request, 'Invalid username or password for admin.')
    else:
        form = AdminLoginForm()
    return render(request, 'admin/admin_login.html', {'form': form})


def adminsignup(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = True
            user.save()
            messages.success(request, 'Admin account created successfully!')
            return redirect('myapp:adminlogin')
    else:
        form = AdminSignupForm()
    return render(request, 'admin/admin_signup.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_admin)
def admin_dashboard(request):
    search_form = SearchForm(request.GET)
    filter_form = FilterForm(request.GET)
    permits = BuildingPermit.objects.all()
    total_applications = permits.count()

    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        if query:
            permits = permits.filter(
                application_number__icontains=query) | permits.filter(
                name__icontains=query) | permits.filter(
                city__icontains=query)

    if filter_form.is_valid():
        if filter_form.cleaned_data.get('application_number'):
            permits = permits.filter(application_number=filter_form.cleaned_data['application_number'])
        if filter_form.cleaned_data.get('name'):
            permits = permits.filter(name__icontains=filter_form.cleaned_data['name'])
        if filter_form.cleaned_data.get('city'):
            permits = permits.filter(city__icontains=filter_form.cleaned_data['city'])
        if filter_form.cleaned_data.get('status'):
            permits = permits.filter(application_status=filter_form.cleaned_data['status'])

    for permit in permits:
        user = CustomUser.objects.get(pk=permit.user_id)
        permit.username = user.username

    context = {
        'search_form': search_form,
        'filter_form': filter_form,
        'permits': permits,
        'total_applications': total_applications,
    }

    return render(request, 'admin/admin_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin)
def admin_approve_permit(request, permit_id):
    permit = get_object_or_404(BuildingPermit, pk=permit_id)
    permit.application_status = 'approved'
    permit.save()
    messages.success(request, f'Application {permit.application_number} approved successfully!')
    return redirect('myapp:admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_admin)
def admin_reject_permit(request, permit_id):
    permit = get_object_or_404(BuildingPermit, pk=permit_id)
    permit.application_status = 'rejected'
    permit.save()
    messages.success(request, f'Application {permit.application_number} rejected.')
    return redirect('myapp:admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_admin)
def application_details(request, permit_id):
    permit = get_object_or_404(BuildingPermit, pk=permit_id)
    return render(request, 'admin/application_details.html', {'permit': permit})


def privacy_policy(request):
    return render(request, 'privacy_policy/privacy_policy.html')


def about(request):
    return render(request, 'about/about.html')


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
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
            return render(
                request,
                'building_permit/result.html',
                {
                    'trees_required': permit.trees_required
                }
            )
    else:
        form = BuildingPermitForm(initial={'user_id': int(request.user.id)})
    return render(request, 'building_permit/apply.html', {'form': form})


def debug_result_page(request):
    return render(request,
                  'building_permit/result.html',
                  {
                      'trees_required': 4
                  }
                  )


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:home')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})


def application_details(request, permit_id: int) -> HttpResponse:
    permit = get_object_or_404(BuildingPermit, pk=permit_id, user_id=request.user.id)
    return render(request, 'home/applications/application_details.html', {'permit': permit})
