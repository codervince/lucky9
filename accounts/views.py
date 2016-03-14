from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, UserProfileEditForm
from .models import UserProfile
from datetime import datetime
from pytz import timezone
import pytz

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                           'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = UserProfile.objects.create(user=new_user)
            return render(request,
                          'accounts/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = UserProfileEditForm(instance=request.user.userprofile,
                                       data=request.POST,)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)
    return render(request, 'accounts/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})

@login_required
def dashboard(request):
    fmt = '%Y-%m-%d %H:%M:%S'
    today = datetime.now()

    # london_now = datetime.now(lontz)
    lon = timezone('Europe/London')
    hkg = timezone('Asia/Hong_Kong')
    syd = timezone('Australia/Sydney')

    london_now_ = lon.localize(today)
    london_now = london_now_.strftime(fmt)

    hongkong_now_ = london_now_.astimezone(hkg)
    hongkong_now = hongkong_now_.strftime(fmt)
    sydney_now = hongkong_now_.astimezone(syd).strftime(fmt)

    params = {
    'section': 'dashboard',
    'today': today,
    'london': london_now,
    'sydney': sydney_now,
    'hongkong': hongkong_now
    }
    return render(request, 'accounts/dashboard.html', params)
