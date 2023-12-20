from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from accounts.forms import LoginForm, ProfileEditForm, UserRegistrationForm, UserEditForm, Profile
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from accounts.models import Profile
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        'user':user,
        'profile':profile
    }
    return render(request, 'profile.html', context)


def user_login(request):
    if request.method =="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username = data['username'],
                                         password = data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Muvaffaqiyatli login amalga oshirildi!!!")
                else:
                    return HttpResponse(" Sizning profilingiz faol holatda emas")
            
            else:
                return HttpResponse("Login yoki parolda xatolik mavjud!")
        else:
            return HttpResponse("Login yoki parolda xatolik mavjud!")
    else:
        form = LoginForm()
        context = {
            'form':form
        }
        return render (request, 'accounts/login.html', context)


def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user = new_user)
            context = {
                "new_user":new_user
            }
            return render(request, "registration/register_done.html", context)
    else:
        form = UserRegistrationForm()
        context = {
            "form":form
        }
    return render(request, "registration/register_form.html", context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy ('login')
    template_name = 'registration/register_form.html'


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data = request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data = request.POST, files = request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        "user_form":user_form,
        "profile_form":profile_form
    }
    return render(request, "registration/profile_edit.html", context)


class Edit_UserView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context = {
        "user_form":user_form,
        "profile_form":profile_form
        }
        return render(request, "registration/profile_edit.html", context)

    def post(self,request):
        user_form = UserEditForm(instance=request.user, data = request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data = request.POST, files = request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')


@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page(request):
    admin_users = User.objects.filter(is_superuser = True)
    context = {
        'admin_users':admin_users
    }

    return render(request, 'admin_page.html', context)