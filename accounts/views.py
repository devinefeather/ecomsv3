from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import logout


# Create your views here.
class loginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username = username, password = password)
            if user is not None:
                auth.login(request, user)

                return redirect('app:index')
        messages.error(request, 'Invalid credentials, try again')
        return render(request,'accounts/login.html')
                        

class registrationView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        conform_password = request.POST['conform_password']



        context = {
            'fieldvalues':request.POST
        }

        if not User.objects.filter(username = username).exists():
            if not User.objects.filter(email = email).exists():

                if len(password) < 6:
                    messages.error(request, 'password too short')
                    return render(request, 'accounts/register.html', context)
                
                user = User.objects.create_user(first_name = first_name, email = email, last_name = last_name, username = username)
                user.set_password(password)
                user.is_active = True
                user.save()
            
        return redirect('app:index')

    

class logoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'accounts/login.html')