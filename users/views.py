from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests


@login_required
def home(request):
    joke = fetch_joke()
    return render(request, 'users/home.html', {'joke': joke})

def fetch_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return f"{data['setup']} - {data['punchline']}"
        else:
            return "Failed to fetch joke"
    except requests.exceptions.RequestException as e:
        return f"Couldn't fetch a joke: {str(e)}"

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Replace 'home' with your desired URL name
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})