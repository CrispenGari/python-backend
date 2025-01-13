from django.shortcuts import render, redirect
from .forms import UserRegisterForm
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
    return render(request, 'users/profile.html')