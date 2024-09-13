from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Registration
from .forms import EventForm, RegistrationForm, UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

def index(request):
    return render(request, 'index.html')

def event_list(request):
    query = request.GET.get('q')
    if query:
        events = Event.objects.filter(
            Q(text__icontains=query) | Q(location__icontains=query)
        ).order_by('-created_at')
    else:
        events = Event.objects.all().order_by('-created_at')
    return render(request, 'event_list.html', {'events': events})

@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})

@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id, user=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'event_confirm_delete.html', {'event': event})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    registered = Registration.objects.filter(event=event, user=request.user).exists()
    return render(request, 'event_detail.html', {'event': event, 'registered': registered})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('event_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.event = event
            registration.save()
            return redirect('registration_success')
    else:
        form = RegistrationForm(initial={'event': event})
    return render(request, 'register_for_event.html', {'form': form, 'event': event})

@login_required
def registration_success(request):
    return render(request, 'event_register.html')

@login_required
def registered_events(request):
    registrations = Registration.objects.filter(user=request.user).select_related('event')
    events = [registration.event for registration in registrations]
    return render(request, 'registered_events.html', {'events': events})

@login_required
def cancel_registration(request, event_id):
    registrations = Registration.objects.filter(event_id=event_id, user=request.user)
    if request.method == 'POST':
        registrations.delete()
        return redirect('registered_events')
    return render(request, 'cancel_registration.html', {'registrations': registrations})
