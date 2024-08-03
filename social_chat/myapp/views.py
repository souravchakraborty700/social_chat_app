from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Interest, Message

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
    return redirect('chat_box', interest_id=interest.id)

@login_required
def chat_box(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id, accepted=True)
    if request.user not in [interest.sender, interest.recipient]:
        print("lets see interest.sender, interest.recipeint", interest.sender, interest.recipient)
        return redirect('received_interests')
    return render(request, 'D:\\chat_app\\social_chat\\myapp\\templates\\myapp\\chatbox.html', {'interest': interest, 'user': request.user})
    

@login_required
def reject_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id, recipient=request.user)
    interest.rejected = True
    interest.save()
    messages.success(request, 'Interest rejected')
    return redirect('received_interests')

@login_required
def send_message(request, interest_id):
    if request.method == 'POST':
        interest = get_object_or_404(Interest, id=interest_id)
        message = request.POST['message']
        Message.objects.create(interest=interest, sender=request.user, content=message)
        return redirect('chat_box', interest_id=interest.id)
    
# views.py
@login_required
def send_message(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    if request.method == 'POST':
        text = request.POST.get('text')  # Ensure 'text' matches the Message model field name
        if text:
            message = Message(interest=interest, sender=request.user, text=text)
            message.save()
            return redirect('chat_box', interest_id=interest.id)
    return render(request, 'D:\\chat_app\\social_chat\\myapp\templates\\myapp\\chatbox.html', {'interest': interest})


def home(request):
    user = request.user
    if user.is_authenticated:
        messages.success(request, f'Welcome Back {user.username}!')
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
