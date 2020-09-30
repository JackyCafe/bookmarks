from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.http import HttpResponse
from django.shortcuts import render
from account.forms import LoginForm, UserRegistrationForm, ProfileEditForm
from django.contrib.auth.models import User


def user_login(request):
    user : User
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                            username = cd['username'],
                            password=cd['password'])
            print()
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse(f'Disable account {cd["username"]} {cd["password"]}')
    else:
        form = LoginForm()
        return render(request,'account/login.html',{'form':form})


@login_required
def dashboard(request):
    return render(request,'account/dashboard.html'
                  ,{'section':'dashedboard'})


def register(request):
    new_user:User
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid() :
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,'account/register_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request,'account/register.html',{'user_form':user_form})



@login_required
def edit(request):
    if request.method == 'POST':
        user_form = ProfileEditForm(instance = request.user,data = request.POST )
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            
