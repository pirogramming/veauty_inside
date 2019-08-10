from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import SignupForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('custom features', {'fields': ('realname', 'nickname', 'gender', 'birth')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('custom features', {
            'fields': ('realname', 'nickname', 'gender', 'birth',),
        }),
    )
    add_form = SignupForm


admin.site.register(User, UserAdmin)