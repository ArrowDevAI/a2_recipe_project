from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm  
from django.shortcuts import render,redirect

def Main(request):
    return render(request, 'home/home.html')

def login_view(request):
    error_message = None
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password=password)
            if user is not None:
                login(request,user)
                return redirect('recipes:list')
        else:
            error_message = 'Something Went Wrong When Validating the User'
    context = {
    'form' : form,
    'error_message' : error_message
        }
    return render(request,'auth/login.html', context)
def logout_view(request):
    logout(request)
    return redirect('logout_success')

def logout_success_view(request):
    return render(request,'auth/logout.html')
