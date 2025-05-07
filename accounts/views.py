from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template,render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
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
        userObj.is_active = False

        userObj.save()

        # token and uid 
        htmly = get_template()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(userObj.pk))
        current_site = get_current_site(request)
        activation_link = f"http://{current_site.domain}/activate/{uid}/{token}"

        # html_messages
        html_message = render_to_string('activation_email.html', {
            'user':userObj,
            'activation_link':activation_link,
        })


        send_mail(
            'activate_your_account',
            html_message,
            settings.DEFAULT_FROM_EMAIL,
            [userObj.email],
            fail_silently = False,

        )

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


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('dokan/index.html')
    else:
        messages.error(request, 'Activation failed please signup again!!!')
        return redirect('signup_view')