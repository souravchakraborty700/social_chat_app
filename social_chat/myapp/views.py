from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'D:\\chat_app\\social_chat\\myapp\\templates\\myapp\\home.html')

# Create your views here.
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            # print("lets see user", user)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'D:\\chat_app\\social_chat\\myapp\\templates\\myapp\\register.html', {'form': form})







