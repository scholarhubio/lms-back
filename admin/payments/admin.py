from django.contrib import admin
from payments.models import Subscription
from config.admin import MyNestedModelAdmin


@admin.register(Subscription)
class SubscriptionAdmin(MyNestedModelAdmin):
    raw_id_fields = ('user', 'course_module')
