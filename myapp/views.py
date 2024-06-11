from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def login_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'm/login_signup.html', {'form': form})

def home(request):
    user_name = "uanme"
    return render(request, 'm/home.html', {'user_name': user_name})

def admin_page(request):
    if not request.user.is_staff:
        return redirect('home')
    return render(request, 'admin_page.html')
