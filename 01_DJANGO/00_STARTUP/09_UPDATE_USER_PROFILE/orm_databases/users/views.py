from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    context = {
        "form": UserRegisterForm()
    }
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        context["form"] = form 
        if form.is_valid():
            # save to the database
            form.save()
            username = form.cleaned_data.get('username')
            # message flashing
            messages.success(request, f'Account created for {username}, Now you can login to the app!')
            return redirect('login')
    return render(request, "users/register.html", context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)