from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "is_staff",
        "is_active",
    ]

    fieldsets = UserAdmin.fieldsets
    fieldsets[1][1]["fields"] = ("first_name", "last_name", "email")
    add_fieldsets = UserAdmin.add_fieldsets
    add_fieldsets[0][1]["fields"] = ("email", "password", "password2")


admin.site.register(CustomUser, CustomUserAdmin)
