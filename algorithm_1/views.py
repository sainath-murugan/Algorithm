from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import VaultForm, FeedBackForm
from django.shortcuts import get_object_or_404
from .models import Vault, History
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.core.mail import EmailMessage
from user.forms import AccountSettings, DeleteAccount


CustomUser = get_user_model()

 
def home(request):
    users = CustomUser.objects.count()
    context = {
        'users':users
    }
    return render(request,'home.html',context)


@login_required(login_url='account_login')
def dashboard(request, id):
    
    current_user = get_object_or_404(CustomUser, id=id)
    if current_user != request.user:                   
        return HttpResponseBadRequest('error 404')
    else:
        form = VaultForm()
        if request.method == "POST":
            form = VaultForm(request.POST)
            if form.is_valid():
                save_form = form.save(commit=False)
                save_form.user = request.user
                form.save()
                return redirect("dashboard" ,id=str(request.user.id))
        items = Vault.objects.all().filter(user=request.user)
        context = {
        'form':form,
        'items':items,
        }
        return render(request,'dashboard.html',context)


@login_required(login_url='account_login')
def delete_password(request, id):

    object = get_object_or_404(Vault, id=id)
    if object.user.id != request.user.id:
        return HttpResponseBadRequest('error 404')
    else:
        if request.method == 'POST':
            Vault.objects.get(id=id).delete()
            return redirect("dashboard" ,id=str(request.user.id))
            
        else:
            context = {
                'object':object
            }
        return render(request,'delete_password.html', context)


@login_required(login_url='account_login')
def edit_password(request, id):
    
    object = get_object_or_404(Vault, id=id)
    if object.user.id != request.user.id:
        return HttpResponseBadRequest('error 404')
    else:
        form = VaultForm()
        if request.method == 'POST':
            form = VaultForm(request.POST, instance=object)
            if form.is_valid():
                form.save()
                return redirect("dashboard" ,id=str(request.user.id))
        else:
            context = {
                'object':object,
                'form':form
            }
        return render(request,'edit_password.html', context)

# from django.core.mail import send_mail
@login_required(login_url='account_login')
def view_password(request, id):

    object = get_object_or_404(Vault, id=id)
    if object.user.id == request.user.id:     
        email = EmailMessage('The password requested by you,',
        f"key: {object.key}, password: {object.value}", 
        to=[request.user.email])
        email.send()
    else:
        return HttpResponseBadRequest('error 404')
    messages.success(request, 'we have sent you a email with key and password')
    return redirect("dashboard" ,id=str(request.user.id))


@login_required(login_url='account_login')
def settings(request, id):

    current_user = get_object_or_404(CustomUser, id=id)
    if current_user == request.user:  
        form = AccountSettings(instance=request.user)

        logged_in_history = History.objects.all().filter(user=request.user)
        objects = Vault.objects.all().filter(user=request.user)

        if request.method == 'POST':
            form = AccountSettings(request.POST, instance=current_user)
            if form.is_valid():
                form.save()
                return redirect('settings',id=str(request.user.id))

        context = {
        'logged_in_history': logged_in_history,
        'form':form,
        'objects':objects
        }
        return render(request, 'view_account.html', context)
    else:
        return HttpResponseBadRequest('error 404')


@login_required(login_url='account_login')
def delete_account(request, id):

    current_user = get_object_or_404(CustomUser, id=id)
    form = DeleteAccount(request=request)  #request=request is due to deletaccount form class
    if current_user == request.user:
        if request.method == 'POST':
            form = DeleteAccount(request.POST, request=request) #request=request is due to deletaccount form class
            if form.is_valid():
                CustomUser.objects.get(id=request.user.id).delete()
                return redirect('home')
        context = {
            'form':form
        }
        return render(request, 'delete_account.html', context)
    else:
        return HttpResponseBadRequest('error 404')
    

@login_required(login_url='account_login')
def feedback(request, id):

    current_user = get_object_or_404(CustomUser, id=id)
    if current_user == request.user:
        form = FeedBackForm()
        if request.method == 'POST':
            form = FeedBackForm(request.POST)
            if form.is_valid():
                save_form = form.save(commit=False)
                save_form.user = request.user
                form.save()
                return redirect("dashboard" ,id=str(request.user.id))

        context = {
            'form':form
        }
        return render(request, 'contact.html', context)
    else:
        return HttpResponseBadRequest('error 404')
    

@login_required(login_url='account_login')
def delete_login_history(request, id):
    current_user = get_object_or_404(CustomUser, id=id)
    if current_user == request.user:
        if request.method == 'POST':
            request.user.profile_user_history.all().delete()
            return redirect("settings" ,id=str(request.user.id))
        else:
            return redirect("settings" ,id=str(request.user.id))
    else:
        return HttpResponseBadRequest('error 404')