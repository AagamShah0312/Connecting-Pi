from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ChatMessage, HireRequest, Skill, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Connecting Pie", {"fields": ("role", "degree", "business_name", "bio", "location", "avatar_initials")}),)
    list_display = ("username", "email", "role", "is_active")
    list_filter = ("role", "is_active")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "provider", "category", "featured")
    list_filter = ("category", "featured")
    search_fields = ("name", "description", "provider__username")


@admin.register(HireRequest)
class HireRequestAdmin(admin.ModelAdmin):
    list_display = ("skill", "receptor", "status", "created_at")
    list_filter = ("status",)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("hire_request", "sender", "created_at")
    search_fields = ("body", "sender__username")
