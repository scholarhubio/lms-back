from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Profile, User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission
from config.admin import BaseModelAdmin, BaseStackedInline


class UserProfileInline(BaseStackedInline):
    model = Profile
    extra = 0
    change_form_template = 'users/admin/change_form.html'


class CustomizedUserAdmin(UserAdmin, BaseModelAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'user_permissions', 'groups',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('phone_number', 'first_name', 'last_name',)
    search_fields = ['phone_number', 'first_name', 'last_name',]
    list_filter = ('role',)
    list_per_page = 10
    inlines = [UserProfileInline,]

admin.site.register(User, CustomizedUserAdmin)