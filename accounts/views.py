from django.shortcuts import render, redirect
from .forms import LoginForm , RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, 'Seni tekrar görmek ne güzel, {}!'.format(request.user))

        return redirect('post_list')

    return render(request, "blog/form.html", {"form": form, 'title': 'Beni içeri alın','title2': 'Sen de kimsin?' ,})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        # user.is_staff = user.is_superuser = True
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        messages.success(request, 'Aramıza hoşgeldin, {}!'.format(request.user))

        return redirect('post_list')

    return render(request, "blog/form.html", {"form": form, 'title': 'Artık ben de sizdenim','title2': 'Size katılayım',})


def logout_view(request):
    logoutuser=request.user
    logout(request)
    messages.success(request, 'Güç seninle olsun, {}! Hoşçakal.'.format(logoutuser))

    return redirect('post_list')