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
# views.py in your Django app
from django.views.generic import TemplateView

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
    return render(request, 'myapp/send_interest.html', {'recipient': recipient})

@login_required
def received_interests(request):
    interests = request.user.received_interests.filter(accepted=False, rejected=False)
    return render(request, 'myapp/received_interests.html', {'interests': interests})

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
    return render(request, 'myapp/chatbox.html', {'interest': interest})


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
    users = User.objects.exclude(id=request.user.id)
    user_data = []

    for user in users:
        sent_interest = Interest.objects.filter(sender=request.user, recipient=user).first()
        received_interest = Interest.objects.filter(sender=user, recipient=request.user).first()
        
        if sent_interest and sent_interest.accepted:
            status = 'contact'
        elif received_interest and received_interest.accepted:
            status = 'contact'
        elif sent_interest:
            status = 'sent'
        else:
            status = 'none'
        
        user_data.append({'id': user.id, 'username': user.username, 'status': status})

    return JsonResponse(user_data, safe=False)


@login_required
def api_received_interests(request):
    interests = Interest.objects.filter(recipient=request.user, accepted=False, rejected=False).values('id', 'sender__username', 'message')
    return JsonResponse(list(interests), safe=False)

@csrf_exempt
@login_required
def api_accept_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id, recipient=request.user)
    interest.accepted = True
    interest.save()
    return JsonResponse({'status': 'accepted', 'interest_id': interest.id})

@csrf_exempt
@login_required
def api_reject_interest(request, interest_id):
    try:
        interest = Interest.objects.get(id=interest_id, recipient=request.user)
        interest.delete()  # or you can set a `rejected` status instead of deleting
        return JsonResponse({'status': 'rejected'})
    except Interest.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Interest not found'}, status=404)

@login_required
def api_connect(request):
    interests = Interest.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user),
        accepted=True
    ).distinct()

    contacts = []
    for interest in interests:
        contact = interest.recipient if interest.sender == request.user else interest.sender
        # Check if there are unread messages for this interest
        has_new_messages = interest.messages.filter(read=False).exclude(sender=request.user).exists()
        contacts.append({
            'contact': {'username': contact.username},
            'interest_id': interest.id,
            'has_new_messages': has_new_messages,
        })

    return JsonResponse(contacts, safe=False)

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

@csrf_exempt
def api_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logout successful'})
    
# views.py
@login_required
def api_user(request):
    user = {
        'id': request.user.id,
        'username': request.user.username
    }
    return JsonResponse(user)


@login_required
def check_auth(request):
    return JsonResponse({'user': request.user.username})

@login_required
def api_messages(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    # Mark messages as read when they are fetched by the recipient
    Message.objects.filter(interest=interest, read=False).exclude(sender=request.user).update(read=True)
    
    messages = Message.objects.filter(interest=interest).values('sender__username', 'text', 'timestamp')
    formatted_messages = [{'username': message['sender__username'], 'text': message['text'], 'timestamp': message['timestamp']} for message in messages]
    return JsonResponse(formatted_messages, safe=False)


@csrf_exempt
@login_required
def api_send_message(request, interest_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('message')
        interest = get_object_or_404(Interest, id=interest_id)
        message = Message.objects.create(interest=interest, sender=request.user, text=text)
        return JsonResponse({'status': 'Message sent'})

@csrf_exempt
@login_required
def api_send_interest(request, user_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        recipient = get_object_or_404(User, id=user_id)
        message = data.get('message', 'Interest sent')  # Get the message from the request body
        interest = Interest(sender=request.user, recipient=recipient, message=message)
        interest.save()
        
        # Notify the recipient
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{recipient.id}',
            {
                'type': 'send_notification',
                'notification': f'{request.user.username}: Wants to connect! Msg: {message}',
                'interest_id': interest.id,
            }
        )

        return JsonResponse({'status': 'Interest sent'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def api_check_auth(request):
    return JsonResponse({'user': {'id': request.user.id, 'username': request.user.username}})


# To server the react app
class IndexView(TemplateView):
    template_name = 'frontend/build/index.html'

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@login_required
def get_chat_partner(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    if request.user == interest.sender:
        chat_partner = interest.recipient
    else:
        chat_partner = interest.sender
    
    return JsonResponse({'username': chat_partner.username})

