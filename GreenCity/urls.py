from django.urls import path
from myapp import views

urlpatterns = [
    path('login/', views.login_signup, name='login_signup'),
    path('home/', views.home, name='home'),
    path('admin_page/', views.admin_page, name='admin_page'),
]
