from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Event,Book
from django.views import View
from .forms import UserSignup, UserLogin,EventForm,BookForm,UserForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone


def home(request):
    return render(request, 'home.html')

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
                  
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")

def event_create(request):
    if request.user.is_anonymous:
        return redirect('login')
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            date=event.date
            time=event.time
            if bool(date==timezone.now().date() and timezone.now().time()<time) ^ bool(date>timezone.now().date()):
                event.organizer = request.user
                event.seats_left = event.capacity
                event.save()
                return redirect('event-list')
            else:
                messages.warning(request, "Please enter valid dates and times.")
                return redirect('event-create')
   
    context = {
        "form":form,
    }
    return render(request, 'create_event.html', context)

def event_book(request,event_id):
    if request.user.is_anonymous:
        return redirect('login')
    event=Event.objects.get(id=event_id)    
    form = BookForm()
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event= event
            if(booking.seats<=event.seats_left and event.seats_left!=0):
                event.seats_left=event.seats_left-booking.seats
                event.save()
                booking.save()
                return redirect('event-list')    
            messages.warning(request, "Can't book more than remaining seats!")    
            return redirect('event-book',event_id)
    context = {
        "form":form,
        "event":event,
    }
    return render(request, 'booking_event.html', context)

def event_list(request):
    if request.user.is_anonymous:
        return redirect('login')    
    events = Event.objects.filter(
            Q(date=timezone.now().date(),time__gt=timezone.now().time())|
            Q(date__gt=timezone.now().date())
            
        ).distinct()
    query = request.GET.get('q')
    if query:        
        events = events.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(organizer__username__icontains=query)
        ).distinct()
    context = {
       "events": events,
    }
    return render(request, 'list.html', context)

def event_detail(request, event_id):
    if request.user.is_anonymous:
        return redirect('login')

    event = Event.objects.get(id=event_id)
    bookings=Book.objects.filter(event=event)
    context = {
        "event": event,
        "bookings":bookings
        
    }
    return render(request, 'detail.html', context)

def no_access(request):
    return render(request, 'no_access.html')

def event_update(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    CAPACITY = event_obj.capacity
    SEATS = event_obj.seats_left

    if not (request.user == event_obj.organizer):
        return redirect('no-access')
    form = EventForm(instance=event_obj)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event_obj)
        if form.is_valid():
            event = form.save(commit=False)
            if CAPACITY <= event.capacity:
                event.seats_left = SEATS + (event.capacity - CAPACITY)
                event.save()
                return redirect('event-list')
            elif CAPACITY > event.capacity:
                messages.warning(request, "Can't set to less than original value!")    
                redirect('event-update', event_id)       
    context = {
        "event_obj": event_obj,
        "form":form,
    }
    return render(request, 'update.html', context) 

def organizer_dashboard(request):
    if request.user.is_anonymous:
        return redirect('login')  
    created_events = Event.objects.filter(organizer=request.user)
    query = request.GET.get('q')
    book=Book.objects.filter(user=request.user)
  
    if query:        
        events = created_events.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(organizer__username__icontains=query)
        ).distinct()
       
    context = {
       "events": created_events,
       "books":book
    }
    return render(request, 'dashboard.html', context)  

def no_access(request):
    return render(request, 'no_access.html')

def event_delete(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    event_obj.delete()
    return redirect('event-list')
    
def book_delete(request, book_id):
    book_obj = Book.objects.get(id=book_id)
    book_obj.event.seats_left=book_obj.seats+book_obj.event.seats_left
    book_obj.event.save()
    book_obj.delete()

    return redirect('dashboard')
def user_update(request, user_id):
    user_obj = User.objects.get(id=user_id)
    form = UserForm(instance=user_obj)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return redirect('event-list')
                  
    context = {
        "user_obj": user_obj,
        "form":form,
    }
    return render(request, 'update1.html', context) 
    
             