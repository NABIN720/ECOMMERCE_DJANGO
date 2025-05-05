from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email','').strip().lower()
        phone = request.POST.get('phone')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.error(request,"Passwords don't match")
            return redirect("signup_view")
        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request,"Invalid email, please use valid email")
            return redirect("signup_view")
        
        if User.objects.filter(username=email).exists():
            messages.error(request,"User already exists, please try with different email!!!")
            return redirect("signup_view")
        

        userObj = User.objects.create_user(username=email, email=email,password=pass1)
        userObj.first_name = fname
        userObj.last_name = lname

        userObj.save()

        messages.success(request,"Your Account has been sucessfully created")

        return redirect('login_view')

    return render(request,'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email','').strip().lower()
        pass1 = request.POST.get('pass1')
        print("All Users:")
        for u in User.objects.all():
            print(f"{u.username} - {u.email} error")

        try:
            # userObj = User.objects.get(email=email)
            print(f"Trying to login: {email=}, {pass1=}")
            user = authenticate(request, username=email, password=pass1)
            print(f"Authenticated user: {user}")

            if user is not None:
                login(request, user)
                return render(request, 'dokan/index.html')
            else:
                messages.error(request, 'Enter correct Credentials')
                return redirect('login_view')

        except User.DoesNotExist:
            messages.error(request, 'User Doesnot Exists, Please Sign Up!!!')
            return redirect('login_view')


    return render(request, 'accounts/login.html')

def logout_view(request):
    return HttpResponse("from logout")


