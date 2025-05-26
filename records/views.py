from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from records.forms import RecordForm
from .models import Record

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to login page after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def add_record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the dashboard after saving
    else:
        form = RecordForm()
    return render(request, 'record_form.html', {'form': form})

@login_required
def add_record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = RecordForm()
    return render(request, 'record_form.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required  # Protect the dashboard so only logged-in users can access it
def dashboard(request):
    query = request.GET.get('q')
    if query:
        records = Record.objects.filter(title__icontains=query) # Search if query exists
    else:
        records = Record.objects.all() # Fetch all records if no search query
    return render(request, 'dashboard.html', {'records': records, 'query': query})

@login_required
def edit_record(request, pk):
    record = Record.objects.get(pk=pk)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = RecordForm(instance=record)
    return render(request, 'record_form.html', {'form': form, 'record': record})

@login_required
def delete_record(request, pk):
    record = Record.objects.get(pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('dashboard')
    return render(request, 'confirm_delete.html', {'record': record})