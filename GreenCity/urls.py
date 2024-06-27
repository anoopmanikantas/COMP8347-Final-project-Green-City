from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from myapp import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('building_permit_details/', views.building_permit_details, name='building_permit_details'),
    path('status_details/', views.status_details, name='status_details'),
    # Add other paths as needed
] + staticfiles_urlpatterns()
