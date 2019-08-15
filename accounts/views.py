from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .forms import SignupForm
from .models import User

User = get_user_model()

# Create your views here.
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

@login_required
def profile(request, kind=""):
    contexts = {}
    contexts['taps'] = ['video', 'interested', 'mycosmetic']

    if kind == contexts['taps'][0] or kind == "":
        kind = contexts['taps'][0]
        contexts['videos'] = request.user.video.all()
    elif kind == contexts['taps'][1]:
        contexts['cosmetics'] = request.user.cosmetic.all()
    elif kind == contexts['taps'][2]:
        contexts['my_cosmetics'] = request.user.my_cosmetic.all()
    else:
        return redirect("profile", contexts['taps'][0])
        
    contexts['kind'] = kind
    return render(request, 'accounts/profile.html', contexts)