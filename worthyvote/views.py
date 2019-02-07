from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import View
from .forms import UserForm, LoginForm
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django import forms


def home(request):
    return render(request, 'worthyvote/home.html')


class RegisterFormView(View):
    form_class = UserForm
    template_name = 'worthyvote/registration.html'

    # to display blank form
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'worthyvote/home.html')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # to process and save data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            if not (User.objects.filter(email=email).exists()):
                user.set_password(password)
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account by clicking on the link below.'
                message = render_to_string('worthyvote/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                return render(request, 'worthyvote/registration_success.html')
            else:
                return render(request, 'worthyvote/registration.html', {'form': form,
                                                                        'error_message': 'Email id already registered'})
        else:
            return render(request, 'worthyvote/registration.html', {'form': form})


def registration_success(request):
    return render(request, 'worthyvote/registration_success.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        return render(request, 'worthyvote/email_confirmed.html')
    else:
        return HttpResponse('Activation link is invalid!')


def email_confirmed(request):
    return render(request, 'worthyvote/email_confirmed.html')


def login_user(request):
    if request.user.is_authenticated:
        return render(request, 'worthyvote/home.html')
    else:
        form = LoginForm(None)
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'worthyvote/home.html')
                else:
                    return render(request, 'worthyvote/login.html', {'form': form,
                                                                     'error_message': 'Your account is disabled'})
            else:
                return render(request, 'worthyvote/login.html', {'form': form, 'error_message': 'Invalid credentials'})
        else:
            return render(request, 'worthyvote/login.html', {'form': form})


def logout_user(request):
    form = LoginForm(None)
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'worthyvote/login.html', {'form': form})
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'worthyvote/home.html')
                else:
                    return render(request, 'worthyvote/login.html', {'form': form,
                                                                     'error_message': 'Your account is disabled'})
            else:
                return render(request, 'worthyvote/login.html', {'form': form, 'error_message': 'Invalid credentials'})
        else:
            return render(request, 'worthyvote/login.html', {'form': form})


