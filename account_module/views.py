from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from account_module.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from .models import User
from django.http import Http404, HttpRequest
from utils.email_service import send_email


# Create your views here.
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_password = register_form.cleaned_data.get('password')
            user_email = register_form.cleaned_data.get('email')
            user: bool = User.objects.filter(email__exact=user_email).exists()
            if user:
                register_form.add_error('email', 'this email is repetitious')

            new_user = User(email=user_email, email_active_code=get_random_string(72), is_active=False,
                            username=user_email)
            new_user.set_password(user_password)
            new_user.save()
            send_email('active your account', new_user.email, {'user': new_user}, 'emails/activate_account.html')

            return redirect(reverse('login_page'))







        else:
            context = {
                'register_form': register_form
            }
            return render(request, 'account_module/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'you are is not active')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('password', 'your password or your username is wrong')



            else:
                login_form.add_error('email', 'user with this information is not found')

        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.save()
                return redirect(reverse('login_page'))
            else:
                pass  # make a error
        raise Http404


class ForgotPasswordView(View):

    def get(self, request: HttpRequest):
        forgot_password_form = ForgotPasswordForm()
        context = {
            'forgot_password_form': forgot_password_form
        }
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request: HttpRequest):
        forgot_password_form = ForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            email = forgot_password_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=email).first()
            if not user is None:
                send_email('reset your password', user.email, {'user': user}, 'emails/reset_password.html')

                return redirect(reverse('login_page'))





            else:
                forgot_password_form.add_error('email', 'your email is not available in database')




        else:
            forgot_password_form = ForgotPasswordForm()
            context = {
                'forgot_password_form': forgot_password_form
            }
            return render(request, 'account_module/forgot_password.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))

        reset_password_form = ResetPasswordForm()
        context = {
            'reset_password_form': reset_password_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        if reset_password_form.is_valid():
            user: User = User.objects.filter(email_active_code__iexact=active_code).first()
            if user is None:
                return redirect(reverse('login_page'))
            else:
                password = reset_password_form.cleaned_data.get('password')
                user.set_password(password)
                user.email_active_code = get_random_string(72)
                user.is_active = True
                user.save()
                return redirect(reverse('login_page'))

        else:
            reset_password_form = ResetPasswordForm()
            context = {
                'reset_password_form': reset_password_form
            }
            return render(request, 'account_module/reset_password.html', context)


class LogoutView(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect(reverse('login_page'))
