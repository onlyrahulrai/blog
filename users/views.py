from django.shortcuts import render, redirect
from django.http import HttpResponse


from .forms import NewUserCreationForm

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from .forms import UserUpdateForm, UserProfileUpdateForm

from django.contrib.auth.decorators import login_required

from main.models import Post
# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            form = NewUserCreationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                form.save()
                messages.info(
                    request, f"{username} Your Account Created Succesfully!")
                return redirect('login')
        else:
            form = NewUserCreationForm()
    context = {
        'form': form,
        'title': 'Register'
    }
    return render(request, 'register.html', context)


def mylogin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You'r logged in successfully!")
                return redirect('home')
            else:
                messages.warning(request, "Username OR Password is invalid!!")
    context = {
        'title': 'Login'
    }
    return render(request, 'login.html', context)


def mylogout(request):
    logout(request)
    return render(request, 'logout.html')


@login_required(login_url="login")
def profile(request):
    user = request.user.post_set.all()
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile Updated Successfully!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'total_post': user.count(),
        'posts': list(user)[:5]
    }
    return render(request, 'profile.html', context)
