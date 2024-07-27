from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BuildingPermitForm, SearchForm, AdminLoginForm, AdminSignupForm, CustomAuthenticationForm, \
    CustomUserCreationForm, ContactForm, FilterForm, AdditionalDocumentsUploadForm
from .models import BuildingPermit, CustomUser, ContactModel, UserHistory
from .respository import Repository
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone

repository = Repository()


@login_required()
def home(request):
    repository.user_id = request.user.id
    today = timezone.now().date()

    profile, _ = UserHistory.objects.get_or_create(user=request.user, visit_date=today)
    if not _:
        profile.visit_count += 1
    else:
        profile.visit_count = 1
    profile.save()

    response = render(
        request,
        'home/home.html',
        {
            'applications': repository.get_application_details()
        }
    )
    response.set_cookie(f'visited_user_{request.user.id}_{request.user.username}', 'true')
    return response


def view_all_applications(request):
    repository.user_id = request.user.id
    form = SearchForm(request.GET or None)
    results = repository.get_all_building_permits()
    message = ""
    if len(results) == 0:
        message = "No permits found"
    if form.is_valid():
        query = form.cleaned_data['query']
        # 1. Search for the name first if it exists.
        building_permits = repository.get_building_permits(query=query)
        results = building_permits
        print(results)
        if len(building_permits) == 0:
            message = "No permits found"

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(
                request,
                'home/applications/view_all_applications.html',
                {
                    "form": form,
                    "results": results,
                    'result_count': len(results),
                    'message': message,
                }
            )
    return render(request, 'home/applications/view_all_applications.html',
                  {
                      "form": form,
                      "results": results,
                      'result_count': len(results),
                      'message': message
                  }
                  )


def download_id_proof(request, permit_id: int):
    permit = get_object_or_404(BuildingPermit, id=permit_id)
    return FileResponse(permit.government_id_proof.open(), as_attachment=True)


def download_land_record_document(request, permit_id: int):
    permit = get_object_or_404(BuildingPermit, id=permit_id)
    return FileResponse(permit.land_purchase_record.open(), as_attachment=True)


def download_additional_document_1(request, permit_id: int):
    permit = get_object_or_404(BuildingPermit, id=permit_id)
    return FileResponse(permit.additional_document_1.open(), as_attachment=True)


def download_additional_document_2(request, permit_id: int):
    permit = get_object_or_404(BuildingPermit, id=permit_id)
    return FileResponse(permit.additional_document_2.open(), as_attachment=True)


def user_profile(request):
    return render(request, 'user_profile/user_profile.html', {'user': request.user})


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
            messages.error(request, 'Please correct the error below.')
    else:
        form = AdminLoginForm()
    return render(request, 'admin/admin_login.html', {'form': form})


def contact_list_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ad')  # Redirect to the same page or another page after successful submission
    else:
        form = ContactForm()

    contacts = ContactModel.objects.all()
    return render(request, 'admin/admincontactinfo.html', {'contacts': contacts, 'form': form})


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
            messages.error(request, 'Please correct the error below.')
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

    context = {
        'search_form': search_form,
        'filter_form': filter_form,
        'permits': permits,
        'total_applications': total_applications,
    }

    return render(request, 'admin/admin_dashboard.html', {'permits': permits})


@login_required
@user_passes_test(lambda u: u.is_admin)
def admin_application_details(request, permit_id):
    permit = get_object_or_404(BuildingPermit, pk=permit_id)
    user = permit.usr
    context = {
        'permit': permit,
        'user': user
    }
    return render(request, 'admin/admin_application_details.html', context)


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
    send_rejection_email(permit.usr, permit)
    messages.success(request, f'Application {permit.application_number} rejected.')
    return redirect('myapp:admin_dashboard')


def send_rejection_email(user, permit):
    subject = 'Your Application Has Been Rejected'
    html_message = render_to_string('emails/rejection_email.html', {'user': user, 'permit': permit})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def send_document_resubmit_email(user, permit):
    subject = 'Document Resubmission Required'
    html_message = render_to_string('emails/document_resubmit_email.html', {'user': user, 'permit': permit})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


@login_required
@user_passes_test(lambda u: u.is_admin)
def admin_request_document_resubmit(request, permit_id):
    permit = get_object_or_404(BuildingPermit, pk=permit_id)
    permit.application_status = 'additional'
    permit.save()
    send_document_resubmit_email(permit.usr, permit)
    messages.success(request, f'Document resubmission requested for application {permit.application_number}.')
    return redirect('myapp:admin_dashboard')


@login_required
def resubmit_application(request, permit_id):
    permit = get_object_or_404(BuildingPermit, pk=permit_id, usr=request.user)
    if request.method == 'POST':
        form = BuildingPermitForm(request.POST, request.FILES, instance=permit)
        if form.is_valid():
            permit.application_status = 'submitted'
            permit.is_resubmitted = True
            form.save()
            messages.success(request, 'Application resubmitted successfully.')
            return redirect('myapp:user_dashboard')
    else:
        form = BuildingPermitForm(instance=permit)
    return render(request, 'user/resubmit_application.html', {'form': form, 'permit': permit})


@login_required
def user_dashboard(request):
    permits = BuildingPermit.objects.filter(usr=request.user)
    return render(request, 'user/user_dashboard.html', {'permits': permits})


@login_required
def log_visit(request):
    user = request.user
    history, created = UserHistory.objects.get_or_create(user=user)
    history.visits += 1
    history.visit_date = timezone.now().date()
    history.visit_time = timezone.now().time()
    history.save()
    return redirect('myapp:user_profile')


@login_required
def user_profile(request):
    user = request.user
    visit_records = UserHistory.objects.filter(user=user).order_by('-visit_date')
    return render(request, 'user_profile/user_profile.html', {'user': user, 'visit_records': visit_records})


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
    return area_map[area] * floors_map[floors] * 3


def building_permit_application(request):
    if request.method == 'POST':
        form = BuildingPermitForm(request.POST, request.FILES)
        if form.is_valid():
            permit = form.save(commit=False)
            permit.usr = request.user
            permit.trees_required = calculate_trees(permit.area, permit.floors)
            # TODO: Comment The Line Below Before Pushing The Code
            # permit.application_status = 'additional'
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
        # form = BuildingPermitForm(initial={'user_id': int(0)})
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
    def _get_dict_using(application: BuildingPermit):
        return {
            'permit': application,
            'is_additional_document_1_available': True if application.additional_document_1.name is not "" else False,
            'is_additional_document_2_available': True if application.additional_document_2.name is not "" else False,
        }

    permit = get_object_or_404(BuildingPermit, pk=permit_id, user_id=request.user.id)
    if permit.application_status == 'additional':
        if request.method == 'POST':
            form = AdditionalDocumentsUploadForm(request.POST, request.FILES, instance=permit)
            if form.is_valid():
                document = form.save(commit=False)
                document.application_status = 'submitted'
                document.save()
                permit.additional_document_1 = document.additional_document_1
                permit.additional_document_2 = document.additional_document_2
                permit.save()
                permit = get_object_or_404(BuildingPermit, pk=permit_id, user_id=request.user.id)
                return render(
                    request,
                    template_name='home/applications/application_details.html',
                    context=_get_dict_using(permit)
                )
        else:
            form = AdditionalDocumentsUploadForm()
        return render(request, 'home/applications/application_details.html', {'permit': permit, 'form': form})
    return render(
        request,
        template_name='home/applications/application_details.html',
        context=_get_dict_using(permit)
    )
