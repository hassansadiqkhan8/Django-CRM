from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


#LogIn and HomePage
def home(request):
    records = Record.objects.all()

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged In...")
            return redirect("home")
        else:
            messages.success(request, "Sorry! try again...")
            return redirect("home")
    else:
        return render(request, "home.html", {"records": records})


# LogOut Page
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged Out...")
    return redirect("home")


# Register a new User
def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username= username, password = password)
            login(request, user)
            messages.success(request, "You have successfully Registered. Welcome!")
            return redirect("home")
    else:
        form = SignUpForm()
        return render(request, "register.html", {"form": form})
    return render(request, "register.html", {"form": form})


# Indivisual customer record
def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, "record.html", {"customer_record": customer_record})
    else:
        messages.success(request, "You must be logged in to view this page...")
        return redirect("home")


# Deleting a record
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted successfully...")
        return redirect("home")
    else:
        messages.success(request, "you must be logged in to do that...")
        return redirect("home")
    

# Adding a Record
def add_record(request):
    form  = AddRecordForm(request.POST)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "New Record has been Added...")
                return redirect("home")
        else:
            form = AddRecordForm()

        return render(request, "add_record.html", {"form": form})
    else:
        messages.success(request, "You need to be logged in to do that...")
        return redirect("home")


# Updating a record
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, " Record has been updated...")
            return redirect("home")
        return render(request, "update_record.html", {"form": form})
    else:
        messages.success(request, "you must be loggedIn to do that...")
        return redirect("home")
        