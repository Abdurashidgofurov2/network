from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('uid', 'phone_number', 'username', 'last_name', 'family_name', 'email', 'bio', 'avatar_thumbnail', 'back_image', 'avatar', 'join_date', 'old', 'sex', 'is_active', 'is_admin', 'is_superuser')
    list_filter = ('is_admin', 'is_active', 'is_superuser', 'sex')
    fieldsets = (
        ('Personal info', {'fields': ('phone_number', 'username', 'last_name', 'family_name', 'email', 'bio', 'follow', 'followers', 'avatar_thumbnail', 'back_image', 'avatar', 'join_date', 'old', 'sex')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'username', 'last_name', 'family_name', 'email', 'bio', 'follow', 'followers', 'avatar_thumbnail', 'back_image', 'avatar', 'join_date', 'old', 'sex', 'password1', 'password2', 'is_active', 'is_admin', 'is_superuser'),
        }),
    )
    search_fields = ('phone_number', 'email', 'username', 'last_name')
    ordering = ('phone_number',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
