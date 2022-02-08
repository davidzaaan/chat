from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import RegisterUserForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index', request.user)

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.warning(request, 'User does not exist')
            return render(request, 'users/index.html')

        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index', user.username) # this is the chat page
        else:
            messages.warning(request, 'Wrong username or password')
        
    return render(request, 'users/index.html')

def register_user(request):
    form = RegisterUserForm()
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            print('success')
            messages.success(request, 'User registered successfully!')
        else:
            print('failure')

        
    return render(request, 'users/register.html', {
        'form': form
    })

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')