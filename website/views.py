from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddUserRecord
from .models import UserRecords
# Create your views here.


def home(request):

    user_records = UserRecords.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully Logged in')
            return redirect('home')
        else:
            messages.success(
                request, 'There was an error Logging you in. Please try again...')
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': user_records})


def register_user(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have Successfully Logged in...')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(
        request, 'You have been Logged out...')
    return redirect('home')


def view_record(request, pk):
    if request.user.is_authenticated:
        user_record = UserRecords.objects.get(id=pk)
        return render(request, 'record.html', {'user_record': user_record})
    else:
        messages.success(request, 'Please Log In to View this Record...')
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:

        try:
            UserRecords.objects.get(id=pk).delete()
            messages.success(
                request, f'Record with ID = {pk} deleted Successfully...')
        except ObjectDoesNotExist:
            messages.success(request, 'Error Deleting the Record')
        except Exception as e:
            messages.success(request, 'Error Deleting the Record')
    else:
        messages.success(request, 'Please Log In to Delete this Record...')
    return redirect('home')


def add_record(request):
    form = AddUserRecord(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record Added...')
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    messages.success(request, 'You must Logged In...')
    return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        user_info = UserRecords.objects.get(id=pk)
        form = AddUserRecord(request.POST or None, instance=user_info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record has been Updated...')
            return redirect('home')
        return render(request, 'update_record.html',{'form': form})
    messages.success(request, 'You must Logged In...')
    return redirect('home')
