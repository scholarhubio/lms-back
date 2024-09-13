from django.contrib import admin
from payments.models import Subscription
from config.admin import MyNestedModelAdmin


@admin.register(Subscription)
class SubscriptionAdmin(MyNestedModelAdmin):
    raw_id_fields = ('user', 'course_module')
    search_fields = ['user__phone_number', 'user__first_name', 'user__last_name',]
    list_filter = ('course_module__module',)
