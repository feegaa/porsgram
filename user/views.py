from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from user.forms import UserForm, UserUpdateForm, AvatarUpdateForm
from user.models import UserModel

from django_email_verification import sendConfirm
# Create your views here.


def register(request):
    next_path = request.GET.get('next', '/')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            
            instance           = form.save(commit=False)
            instance.is_active = True
            instance.set_password(request.POST['password'])
            instance.save()

            sendConfirm(instance)


            # user     = UserModel.objects.get(username=username,
            #                              password=password,
            #                             )
            # login(request, user)
            # messages.success(request, 'welcome '+str(username))        
            return redirect(next_path)

    elif request.user.is_authenticated:
        messages.warning(request, 'Logout '+str(request.user.username))        
        return redirect('user:logout')

    else:
        form = UserForm()

    return render(
            request, 
            'user/register.html', 
            context={'form': form}
        )



def index(request):
    return render(request, 'qa/index.html', context=None)


def user(request, id):
    try:
        user = UserModel.objects.get(id=id)
    except ObjectDoesNotExist:
        return redirect('user:index')

    return render(request, 'user/user.html', {"user": user})



def users(request):
    try:
        users = UserModel.objects.all()
        return render(request, 
                    'user/users.html', 
                    context={'users': users})

    except ObjectDoesNotExist:
        return HttpResponseRedirect('/qlog')



def loginView(request):
    next_path = request.GET.get('next', '/')
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print(next)
        try:
            user = UserModel.objects.get(username=username, 
                                        password=password)
            if user is not None:
                login(request, user)
                request.session['id']  = user.id
                messages.success(request, 'welcome '+str(user.username))        
                return redirect(next_path)
        
        except ObjectDoesNotExist:
            messages.error(request, 'نام کاربری و یا رمز عبور اشتباه است.')
    return render(request, 'user/login.html', {})


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

            messages.success(request, 'update')        
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
            'user/dashboard.html', 
            context=context
        )



