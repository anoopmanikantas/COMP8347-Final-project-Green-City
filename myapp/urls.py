from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.contrib.auth import views as auth_views
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

from myapp.views import contact_list_view

app_name = 'myapp'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('building_permit_details/', views.building_permit_details, name='building_permit_details'),
    path('status_details/', views.status_details, name='status_details'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('adminsignup/', views.adminsignup, name='adminsignup'),
    path('admincontactinfo/', views.contact_list_view, name='contact_list'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_application_details/<int:permit_id>/', views.admin_application_details, name='admin_application_details'),
    path('admin_approve/<int:permit_id>/', views.admin_approve_permit, name='admin_approve_permit'),
    path('admin_reject/<int:permit_id>/', views.admin_reject_permit, name='admin_reject_permit'),
    path('admin_request_document_resubmit/<int:permit_id>/', views.admin_request_document_resubmit, name='admin_request_document_resubmit'),
    path('resubmit_application/<int:permit_id>/', views.resubmit_application, name='resubmit_application'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('apply/', views.building_permit_application, name='building_permit_application'),
    path('application_details/<int:permit_id>/', views.application_details, name='application_details'),
    path('view_all_applications', views.view_all_applications, name='view_all_applications'),
    path('download_id_proof/<int:permit_id>/', views.download_id_proof, name='download_id_proof'),
    path('download_land_record/<int:permit_id>/', views.download_land_record_document, name='download_land_record_document'),
    path('download_additional_document_1/<int:permit_id>/', views.download_additional_document_1, name='download_additional_document_1'),
    path('download_additional_document_2/<int:permit_id>/', views.download_additional_document_2, name='download_additional_document_2'),
    path('debug/', views.debug_result_page, name='debug_result_page'),
    path('contact/', views.contact_view, name='contact'),

    # Add other paths as needed

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name ="register/password_reset.html"), name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = "register/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "register/password_reset_form.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = "register/password_reset_done.html"), name='password_reset_complete'),
    path('accounts/login/', views.user_login, name='accounts_login'),

] + staticfiles_urlpatterns()


# staticfiles_urlpatterns()
# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
