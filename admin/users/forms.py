from django import forms
from payments.models import Subscription
from courses.models import CourseModule
from django.db import IntegrityError, transaction


class SubscriptionInlineForm(forms.ModelForm):
    class Meta:
        model = CourseModule
        fields = ['module', 'course']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields, '########')
        self.fields['course_module'].queryset = Subscription.objects.all().exclude(is_deleted=True)

    def save(self, commit=True):
        try:
            with transaction.atomic():
                return super().save(commit=commit)
        except IntegrityError as e:
            # Instead of raising an error, return None and let the admin handle it
            self.add_error(None, "This user module combination already exists.")
            return self.instance
