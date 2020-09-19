from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.views.generic import View
from django.core.paginator import Paginator



from user.forms import UserForm, UserUpdateForm, AvatarUpdateForm, ResetPasswordForm, GetEmailForm
from user.models import UserModel
from user.confirm import verifyToken, sendConfirm
from user.errors import NotAllFieldCompiled
from user.reset import sendResetPasswordEmail

from QA.models import QuestionModel, AnswerModel

from porsgram.path import *
import time

# Create your views here.


def register(request):
    next_path = request.GET.get('next', '/')
    if request.POST :
        form = UserForm(request.POST)
        if form.is_valid():
            
            instance           = form.save(commit=False)
            instance.is_active = False
            instance.set_password(request.POST['password'])
            instance.save()

            sendConfirm(instance)

            messages.success(request, 'ایمیل برای شما ارسال شد' + str(instance.username))        
            return redirect(next_path)

    elif request.user.is_authenticated:
        messages.warning(request, 'خروج '+str(request.user.username))        
        return redirect('user:logout')

    else:
        form = UserForm()

    return render(
            request, 
            USER_REGISTER, 
            context={'form': form}
        )



# def index(request):
#     return render(request, 'qa/index.html', context=None)



def user(request, username):
    try:
        user      = UserModel.objects.get(username=username)
    except ObjectDoesNotExist:
        messages.warning(request, 'همچین کاربری نداریم')
        return redirect('user:users')
    return render(request, USER_USER, {'user': user})




def users(request):
    users       = UserModel.objects.all()    
    paginator   = Paginator(users, 21)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)

    context     = {
        'page_obj': page_obj,
    }

    return render(request, USER_USERS, context=context)
        


def loginView(request):
    next_path = request.GET.get('next', '/')

    if request.user.is_authenticated:
        return redirect('user:logout')

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = authenticate(username=username, 
                                password=password)
            if (user is not None and
                user.is_active) :
                login(request, user)
                request.session['id'] = user.id
                messages.success(request, 'سلام '+str(user.username))        
                return redirect(next_path)
            else:
                messages.info(request, "احتمالا ایمیل شما فعال نشده")        

        except ObjectDoesNotExist:
            messages.error(request, 'نام کاربری و یا رمز عبور اشتباه است.')
    return render(request, USER_LOGIN, {})


@login_required
def logoutView(request):
    try:
        request.session.delete()
        logout(request)
    except KeyError:
        return redirect('user:users')
    return redirect('user:login')



@login_required
def dashboard(request):

    try:
        user = UserModel.objects.get(id=request.user.id)
    except ObjectDoesNotExist:
        return HttpResponse("invalid user_profile!")

    if request.method == "POST" :
        update_user_form   = UserUpdateForm(data=request.POST, instance=user)
        update_avatar_form = AvatarUpdateForm(request.POST, request.FILES, instance=user.avatarmodel)

        if update_user_form.is_valid() and update_avatar_form.is_valid():
            update_avatar_form.save()
            update_user_form.save()

            messages.success(request, 'صفحه شما بروزرسانی شد.')        
            return redirect('user:dashboard')

    else:
        update_user_form = UserUpdateForm(instance=user)
        update_avatar_form = AvatarUpdateForm(instance=user.avatarmodel)

    context = {
        'user_form'  : update_user_form,
        'avatar_form': update_avatar_form,   
        'user'       : user,
    }

    return render(
            request, 
            USER_DASHBOARD, 
            context=context
        )



def confirmEmail(request, email, email_token):
    try:
        template = settings.EMAIL_PAGE_TEMPLATE
        return render(request, template, {'success': verifyToken(email, email_token)})
    except AttributeError:
        raise NotAllFieldCompiled('EMAIL_PAGE_TEMPLATE field not found')



class ResetPasswordView(View):
    form_class = ResetPasswordForm
    template   = settings.EMAIL_RESET_PASSWORD_TEMPLATE

    def get(self, request, *args, **kwargs):
        email       = self.kwargs['email']
        email_token = self.kwargs['email_token']

        if verifyToken(email, email_token):
            form = self.form_class()
            return render(request, self.template, {'form': form})


    def post(self, request, *args, **kwargs):
        form     = self.form_class(request.POST)
        username = self.kwargs['username']

        if form.is_valid():
            try:
                user = UserModel.objects.get(username=username)
                user.set_password(form.cleaned_data) # Deactivate account till it is confirmed
                user.save()

                messages.success(request, ('Please Confirm your email to complete registration.'))
                return redirect('user:login')

            except ObjectDoesNotExist:
                return redirect('user:index')

        else:
            return render(request, self.template, {'form': form})


def getEmailForResetPassword(request):
    

    if request.POST:
        form = GetEmailForm(request.POST)

        if form.is_valid():
            try:
                user = UserModel.objects.get(email=form.cleaned_data['email'])
                sendResetPasswordEmail(user)
                messages.success(request, ('reset password email sent.'))
                return redirect('user:index')
            except ObjectDoesNotExist:
                messages.error(request, ('there is no such email.'))
                return redirect('user:index')

    form = GetEmailForm()
    return render(request, USER_GET_EMAIL, {'form': form})



def getEmailForActivate(request):
    
    if request.user.is_authenticated:
        messages.error(request, ('حساب شما در حال حاضر فعال است'))
        return redirect('user:dasboard')

    if request.POST:
        form = GetEmailForm(request.POST)

        if form.is_valid():
            try:
                user = UserModel.objects.get(email=form.cleaned_data['email'])
                sendConfirm(user)
                messages.success(request, ('ایمیل فعالسازی برای شما ارسال شد'))
                return redirect('user:login')
            except ObjectDoesNotExist:
                messages.error(request, ('اول باید حساب باز کنید، ایمیل موجود نیست.'))

    form = GetEmailForm()
    return render(request, USER_GET_EMAIL, {'form': form})
