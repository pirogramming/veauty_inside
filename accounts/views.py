from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .forms import SignupForm
from .models import User
from beauty.models import Bigcate, Video, Cosmetic

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
        for num in request.POST:
            try:
                video = get_object_or_404(Video, pk=num)
                request.user.video.remove(video)
            except:
                pass
    return redirect("profile", 'video')

@login_required
def cosmetic_scrap_processing(request):
    if request.method == 'POST':
        if request.POST['selection'] == 'cancel':
            if request.POST['kind'] == 'interested':
                for num in request.POST:
                    try:
                        cosmetic = get_object_or_404(Cosmetic, pk=num)
                        request.user.cosmetic.remove(cosmetic)
                    except:
                        pass
            elif request.POST['kind'] == 'mycosmetic':
                for num in request.POST:
                    try:
                        my_cosmetic = get_object_or_404(Cosmetic, pk=num)
                        request.user.my_cosmetic.remove(my_cosmetic)
                    except:
                        pass
        elif request.POST['selection'] == 'combine':
            selected = []
            for num in request.POST:
                    try:
                        cosmetic = get_object_or_404(Cosmetic, pk=num)
                        selected.append(cosmetic)
                    except:
                        pass
            return redirect("beauty:combine_result")
    return redirect("profile", request.POST['kind'])