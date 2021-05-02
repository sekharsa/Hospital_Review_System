from django.shortcuts import render, redirect
from hospitals.forms import HospitalForm
from doctors.forms import DoctorForm
from .forms import UserForm
from django.views import View
from django.contrib import auth
from django.contrib import messages, auth
from django.contrib.auth.models import User
from hospitals.models import Hospital
from django import forms
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from accounts.Utils import token_generator

# Create your views here.

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        print(username, password)
        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            
            return redirect('index')
        else:
           
            return render(request, 'signin_fail.html')

    else:
        return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')


def hospReg(request):
    if request.method == "POST":
        hospform = HospitalForm(request.POST, request.FILES)
        username = request.POST['Username']
        password = request.POST['psw']
        email = request.POST['Email']
        hospreg = request.POST['HospitalRegisterationNumber']

        emailerror = ""
        usernameerror = ""
        regerror = ""

        if User.objects.filter(email=email).exists():
            emailerror = "Email already exists"
        else:
            emailerror = ""
        if User.objects.filter(username=username).exists():
            usernameerror = "Username already exists"
        else:
            usernameerror = ""
        if Hospital.objects.filter(HospitalRegisterationNumber=hospreg).exists():
            regerror = "A hospital is already registered with this registeration number"
        else:
            regerror = ""

        context = {
            "form": hospform,
            "regerror": regerror,
            "emailerror": emailerror,
            "usernameerror": usernameerror,
            "formerror": ""
        }

        if emailerror != "" or usernameerror != "":
            return render(request, 'Hospitalregistion.html', context)

        if hospform.is_valid():
            # Create user
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_active = False
            user.save()

            # Save the Data to the Database 
            hospform.save()

            subject = "Activate Your account"
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64, "token": token})
            activate_url = 'http://'+domain+link
            body = "Hi " + username + "!\n To activate your account please click on this link\n" + activate_url

            Email = send_mail (
                subject,
                body,
                "jeevannakshawad@gmail.com",
                [email],
                fail_silently=False
            )

            #automatically login the user for the firsttime
            user = auth.authenticate(request, username=username, password=password)
            print("User Created")
            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                messages.success(request, 'Activate your account after clicking the link sent to your mail')
                return redirect('index')
        else:
            return render(request, 'Hospitalregistion.html', {"form": hospform, "regerror": "", "emailerror": "", "usernameerror": "", "formerror": hospform.errors})

    else:
        hospform = HospitalForm()
    return render(request, 'Hospitalregistion.html', {"form": hospform, "regerror": "", "emailerror": "", "usernameerror": "", "formerror": ""})

def userReg(request):
    if request.method == "POST":
        userform = UserForm(request.POST, request.FILES)
        username = request.POST['Username']
        password = request.POST['psw']
        email=request.POST['Email']

        emailerror = ""
        usernameerror = ""

        if User.objects.filter(username=username).exists():
            usernameerror = "Username already exists"
        else:
            usernameerror = ""
        if User.objects.filter(email=email).exists():
            emailerror = "Email already exists"
            
        else:
            emailerror = ""
        
        context = {
            "form": userform,
            "emailerror": emailerror,
            "usernameerror": usernameerror,
            "formerror": ""
        }

        if emailerror != "" or usernameerror != "":
            return render(request, 'user_registration.html', context)


        if userform.is_valid():
            # Create user
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_active = False
            user.save()
            
            # Save the Data to the Database 
            userform.save()
            subject = "Activate Your account"
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64, "token": token})
            activate_url = 'http://'+domain+link
            body = "Hi " + username + "!\n To activate your account please click on this link\n" + activate_url

            Email = send_mail (
                subject,
                body,
                "jeevannakshawad@gmail.com",
                [email],
                fail_silently=False
            )
            
            #automatically login the user for the firsttime
            user = auth.authenticate(request, username=username, password=password)
            print("User Created")
            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                messages.success(request, 'Activate your account after clicking the link sent to your mail')
                return redirect('index')
        else:
            return render(request, 'user_registration.html', {"form": userform,  "emailerror": "", "usernameerror": "", "formerror": userform.errors})

    else:
        userform = UserForm()
    return render(request, 'user_registration.html', {"form": userform, "emailerror": "", "usernameerror": "", "formerror": ""})


def docReg(request):
    if request.method == "POST":
        doctorForm = DoctorForm(request.POST, request.FILES)
        username = request.POST['Username']
        password = request.POST['psw']
        email=request.POST['Email']
        print(username)
        if User.objects.filter(username=username).exists():
            return render(request, 'doctor_regestration.html', {"form": doctorForm, "data": "Username Already Exists"})

        if User.objects.filter(email=email).exists():
            return render(request, 'doctor_regestration.html', {"form": doctorForm, "data": "Email Already Exists"})

        if doctorForm.is_valid():
            # Create user
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_active = False
            user.save()
            
            # Save the Data to the Database 
            doctorForm.save()
            subject = "Activate Your account"
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64, "token": token})
            activate_url = 'http://'+domain+link
            body = "Hi " + username + "!\n To activate your account please click on this link\n" + activate_url

            Email = send_mail (
                subject,
                body,
                "jeevannakshawad@gmail.com",
                [email],
                fail_silently=False
            )
            
            #automatically login the user for the firsttime
            user = auth.authenticate(request, username=username, password=password)
            print("User Created")
            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                messages.success(request, 'Activate your account after clicking the link sent to your mail')

                return redirect('index')
        else:
            return render(request, 'doctor_regestration.html', {"form": doctorForm, "data": doctorForm.errors})

    else:
        doctorForm = DoctorForm()
    return render(request, 'doctor_regestration.html', {"form": doctorForm, "data": ""})

def forgPass(request):
    return render(request, 'forgot_password.html')

def signinFail(request):
    return render(request, 'signin_fail.html')
    
def signout(request):
    auth.logout(request)
    
    return redirect('index')

class verificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('index'+'?message'+'User already activated')

            if user.is_active:
                messages.success(request, 'Account is already active')
                return redirect('index')
            user.is_active = True
            user.save()
            auth.login(request, user)
            messages.success(request, 'Account activated successfully')
            return redirect('index')
        except Exception as ex:
            pass
        return redirect('index')