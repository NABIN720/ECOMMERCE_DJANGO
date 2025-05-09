from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template,render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
# Create your views here.

def index(request):
    pass

def signup_view(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email','').strip().lower()
        username = request.POST.get('username')
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
        
        if not username.isalnum():
            messages.error(request,"Username must be alphanumeric")
            return redirect("signup_view")
        
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists, please try with different email!!!")
            return redirect("signup_view")

        userObj = User.objects.create_user(username=username, email=email,password=pass1)
        userObj.first_name = fname
        userObj.last_name = lname
        userObj.is_active = False
        request.session['first_name'] = fname
        request.session['last_name'] = lname

        # userObj.save()

        # token and uid 
        # htmly = get_template()
        token = default_token_generator.make_token(userObj)
        uid = urlsafe_base64_encode(force_bytes(userObj.pk))
        current_site = get_current_site(request)
        activation_link = f"http://{current_site.domain}/accounts/activate/{uid}/{token}"

        # html_messages
        html_message = render_to_string('accounts/activation_email.html', {
            'user':userObj,
            'activation_link':activation_link,
        })
        plain_message = strip_tags(html_message)


        email = EmailMultiAlternatives(
            subject="Activate your Account",
            body = plain_message,
            from_email = settings.DEFAULT_FROM_EMAIL,
            to=[userObj.email],

        )
        email.attach_alternative(html_message, "text/html")
        email.send()

        # send_mail(
        #     'activate_your_account',
        #     html_message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [userObj.email],
        #     fail_silently = False,

        # )

        messages.success(request,"Activation email is sent to you please activate to continue!!!")

        return redirect('login_view')

    return render(request,'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        print("All Users:")
        for u in User.objects.all():
            print(f"{u.username} - {u.email} error")

        try:
            # userObj = User.objects.get(email=email)
            # print(f"Trying to login: {email=}, {pass1=}")
            user = authenticate(request, username=username, password=pass1)
            print(f"Authenticated user: {user}")

            if user is not None:
                print(user)
                login(request, user)
                next_url = request.GET.get('next')
                return redirect(next_url) if next_url else redirect('dokan:index')
            else:
                messages.error(request, 'Enter correct Credentials')
                return redirect('login_view')

        except User.DoesNotExist:
            messages.error(request, 'User Doesnot Exists, Please Sign Up!!!')
            return redirect('dokan:index')
    


    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.first_name = request.session.get('first_name')
        user.last_name = request.session.get('last_name')
        user.is_active = True
        user.save()
        return redirect('login_view')
    else:
        messages.error(request, 'Activation failed please signup again!!!')
        return redirect('signup_view')
    return render(request, 'accounts/login.html')

# def store_user_info(request):
#     request.session['full_name'] = f"{request.user.first_name} {request.user.last_name}"
#     request.session['email'] = request.user.email
#     return redirect('dokan:index')