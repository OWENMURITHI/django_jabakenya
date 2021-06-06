from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render_to_response, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..forms import RegisterForm, User
from ..models import Product
from ..decorators import seller_required

def register(request):
    if request.method == 'POST':
        f = RegisterForm(request.POST)
        if f.is_valid():
            #Save the new user
            f.save()
            messages.success(request, message="Account Created Successfully. You are now logged in!")
            #Get the username and password
            phonenumber = request.POST['phonenumber']
            password = request.POST['password1']
            #Authenticate the user and then login
            new_user = authenticate(phonenumber=phonenumber, password=password)
            login(request, new_user)
            return redirect('home')
    else:
        f = RegisterForm()

    return render (request, 'registration/signup_form.html', {'form':f})



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'jaba/change_password.html', {
        'form': form
    })


@method_decorator([login_required], name='dispatch')
class ProfileView(ListView):
    model = User
    template_name = 'jaba/account.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class ProfileUpdate(UpdateView):
    model = User
    fields = ('username', 'phonenumber', 'email')
    template_name = 'jaba/update_user.html'

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.save()
        messages.success(self.request, 'Personal Information Changed!!!')
        return redirect('profile')