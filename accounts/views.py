from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .forms import SignupForm
from .models import User
from beauty.models import Bigcate, Video, Cosmetic
from beauty.views import create_recomend
import copy
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages

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
        videos = Video.objects.filter(pk__in=request.POST.getlist('video_id')) or ''
        request.user.video.remove(*videos)
        if videos:
            messages.success(request, '선택하신 동영상들이 스크랩 취소되었습니다.')
        else:
            messages.warning(request, '스크랩을 취소할 동영상을 선택해주세요.')
    return redirect("profile", 'video')

@login_required
def cosmetic_scrap_processing(request):
    if request.method == 'POST':
        cosmetics_list = request.POST.getlist('cosmetic_id') or ''
        if not cosmetics_list:
            messages.warning(request, '화장품을 선택해주세요.')
            return redirect("profile", request.POST['kind'])

        elif request.POST['selection'] == 'cancel':
            cosmetics = Cosmetic.objects.filter(pk__in=cosmetics_list)
            if request.POST['kind'] == 'interest':
                request.user.cosmetic.remove(*cosmetics)
                messages.success(request, '선택하신 화장품을 관심 화장품에서 제거했습니다.')
            elif request.POST['kind'] == 'my':
                request.user.my_cosmetic.remove(*cosmetics)
                messages.success(request, '선택하신 화장품을 내 화장품에서 제거했습니다.')
        elif request.POST['selection'] == 'combine':
            querystring = (lambda x: '?c=' + '&c='.join(x) if x else "?")(cosmetics_list)

            response = redirect("beauty:combine_result")
            response['Location'] += querystring
            return response
            
    return redirect("profile", request.POST['kind'])


class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('profile')
    template_name = 'accounts/password_change.html'

    def form_valid(self, form):
        messages.info(self.request, '암호 변경을 완료했습니다.')
        return super().form_valid(form)


# class MyNicknameChangeView(User):
#     class Meta:
#         model = get_user_model()
#         fields = ['nickname']