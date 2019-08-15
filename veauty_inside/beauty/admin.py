from django.contrib import admin
from .models import Youtuber, Video, Cosmetic #, Viuser

# Register your models here.
@admin.register(Youtuber)
class YoutuberAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'youtuber', 'upload_at']

@admin.register(Cosmetic)
class CosmeticAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']

# @admin.register(Viuser)
# class ViuserAdmin(admin.ModelAdmin):
#     list_display = ['name']

