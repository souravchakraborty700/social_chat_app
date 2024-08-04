from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Interest, Message
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q
from django.http import JsonResponse
from django.db import models
import json

def index(request):
    return render(request, 'myapp/index.html')

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    contacts = []
    for user in users:
        is_contact = Interest.objects.filter(
            (Q(sender=request.user) & Q(recipient=user)) |
            (Q(sender=user) & Q(recipient=request.user)),
            accepted=True
        ).exists()
        contacts.append((user, is_contact))

    return render(request, 'myapp/user_list.html', {'contacts': contacts})

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

    # Notify the sender
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{interest.sender.id}',
        {
            'type': 'send_notification',
            'notification': f'{request.user.username} accepted your interest. Click here to chat.',
            'interest_id': interest.id,
        }
    )

    messages.success(request, 'Interest accepted')
    return redirect('chat_box', interest_id=interest.id)

# views.py
@login_required
def chat_box(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id, accepted=True)
    if request.user not in [interest.sender, interest.recipient]:
        return redirect('received_interests')
    
    # Mark messages as read
    interest.messages.filter(sender=interest.sender if interest.recipient == request.user else interest.recipient).update(read=True)
    
    return render(request, 'myapp/chatbox.html', {'interest': interest, 'user': request.user})

    

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

@login_required
def connect(request):
    accepted_interests = Interest.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user),
        accepted=True
    ).distinct()

    contacts = []
    for interest in accepted_interests:
        contact = interest.recipient if interest.sender == request.user else interest.sender
        has_new_messages = interest.messages.filter(read=False).exclude(sender=request.user).exists()
        contacts.append({
            'contact': contact,
            'interest_id': interest.id,
            'has_new_messages': has_new_messages,
        })

    return render(request, 'myapp/connect.html', {'contacts': contacts})

@login_required
def api_user_list(request):
    users = User.objects.exclude(id=request.user.id).values('id', 'username')
    return JsonResponse(list(users), safe=False)

@login_required
def api_received_interests(request):
    interests = Interest.objects.filter(recipient=request.user, accepted=False, rejected=False).values('id', 'sender__username', 'message')
    return JsonResponse(list(interests), safe=False)

@login_required
def api_accept_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id, recipient=request.user)
    interest.accepted = True
    interest.save()
    return JsonResponse({'status': 'accepted'})

@login_required
def api_reject_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id, recipient=request.user)
    interest.rejected = True
    interest.save()
    return JsonResponse({'status': 'rejected'})

@login_required
def api_connect(request):
    contacts = Interest.objects.filter(accepted=True).filter(models.Q(sender=request.user) | models.Q(recipient=request.user)).values('id', 'sender__username', 'recipient__username')
    return JsonResponse(list(contacts), safe=False)


@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        
@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already taken'}, status=400)
        else:
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'message': 'User registered successfully'})

def api_logout(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})