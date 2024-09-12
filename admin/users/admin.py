from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Profile, User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission


class UserProfileInline(admin.StackedInline):
    model = Profile
    extra = 0
    change_form_template = 'users/admin/change_form.html'


class CustomizedUserAdmin(UserAdmin):
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
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'phone_number')
    search_fields = ['phone', 'first_name', 'last_name',]
    list_per_page = 10
    inlines = [UserProfileInline,]

admin.site.register(User, CustomizedUserAdmin)