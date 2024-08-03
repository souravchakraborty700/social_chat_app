from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Interest

def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'D:\\chat_app\\social_chat\\myapp\\templates\\myapp\\user_list.html', {'users': users})

@login_required
def send_interest(request, user_id):
    recipient = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        message = request.POST['message']
        interest = Interest(sender=request.user, recipient=recipient, message=message)
        interest.save()
        messages.success(request, f'Interest sent to {recipient.username}')
        return redirect('user_list')
    return render(request, 'D:\\chat_app\\social_chat\\myapp\\templates\\myapp\\send_interest.html', {'recipient': recipient})

@login_required
def received_interests(request):
    interests = request.user.received_interests.filter(accepted=False, rejected=False)
    return render(request, 'D:\\chat_app\\social_chat\\myapp\\templates\\myapp\\received_interests.html', {'interests': interests})

@login_required
def accept_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id, recipient=request.user)
    interest.accepted = True
    interest.save()
    messages.success(request, 'Interest accepted')
    return redirect('received_interests')

@login_required
def reject_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id, recipient=request.user)
    interest.rejected = True
    interest.save()
    messages.success(request, 'Interest rejected')
    return redirect('received_interests')

def home(request):
    
    return render(request, 'myapp/home.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome, {username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
