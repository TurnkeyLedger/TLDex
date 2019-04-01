from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from registration.forms  import CustomUserCreationForm
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account created successfully')
            form.save()
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form':form})