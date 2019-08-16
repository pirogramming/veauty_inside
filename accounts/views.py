from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .forms import SignupForm
from .models import User
from beauty.models import Bigcate, Video, Cosmetic
from beauty.views import create_recomend
import copy

User = get_user_model()


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name="accounts/signup.html"

    def get_success_url(self):
        next_url = self.request.GET.get('next') or 'profile'
        return resolve_url(next_url)

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        return redirect(self.get_success_url())

signup = SignupView.as_view()

class LoginView(auth_views.LoginView):
    template_name="accounts/login.html"
    redirect_authenticated_user = True

login = LoginView.as_view()

@login_required
def profile(request, kind=""):
    contexts = {}
    contexts['taps'] = ['video', 'interest', 'my']
    contexts['kind'] = kind

    if kind == contexts['taps'][0] or kind == "":
        kind = contexts['taps'][0]
        contexts['kind'] = kind
        contexts['videos'] = request.user.video.all()
        contexts['big_categories'] = Bigcate.objects.all()

        return render(request, 'accounts/video_table.html', contexts)
    elif kind == contexts['taps'][1]:
        contexts['cosmetics'] = request.user.cosmetic.all()

        return render(request, 'accounts/cosmetic_table.html', contexts)
    elif kind == contexts['taps'][2]:
        contexts['cosmetics'] = request.user.my_cosmetic.all()

        return render(request, 'accounts/cosmetic_table.html', contexts)
    else:
        return redirect("profile", contexts['taps'][0])

@login_required
def video_scrap_processing(request):
    if request.method == 'POST':
        videos = Video.objects.filter(pk__in=request.POST.getlist('video_id'))
        request.user.video.remove(*videos)
    return redirect("profile", 'video')

@login_required
def cosmetic_scrap_processing(request):
    if request.method == 'POST':
        if request.POST['selection'] == 'cancel':
            cosmetics = Cosmetic.objects.filter(pk__in=request.POST.getlist('cosmetics_id'))
            if request.POST['kind'] == 'interest':
                request.user.cosmetic.remove(*cosmetics)
            elif request.POST['kind'] == 'my':
                request.user.my_cosmetic.remove(*cosmetics)
        elif request.POST['selection'] == 'combine':
            querystring = (lambda x: '?c=' + '&c='.join(x) if x else "?")(request.POST.getlist('cosmetic_id'))

            response = redirect("beauty:combine_result")
            response['Location'] += querystring
            return response
            
    return redirect("profile", request.POST['kind'])
