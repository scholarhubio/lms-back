from django import forms
from courses.models import Module


class ModuleAdmin(forms.ModelForm):
    module = forms.ModelMultipleChoiceField(
        queryset=Module.objects.all(),
        widget=forms.SelectMultiple,
        required=False
    )

    def get_initial_for_field(self, field, field_name):
        """
        Mark current groups of student in Admin panel
        """
        if self.instance and self.instance.id and hasattr(self.instance, 'modules'):
            modules = tuple([x.id for x in self.instance.modules.all()])
            self.fields['module'].initial = modules

            return super().get_initial_for_field(field, field_name)

    def save(self, commit=True):
        """
        Redefined save method to support Multiple Choice of groups in Admin panel
        """
        instance = super().save(commit=False)
        if commit:
            instance.save()
        instance.modules.set(self.cleaned_data['module'])
        # Add a method to the form to allow deferred
        # saving of m2m data.
        self.save_m2m = self._save_m2m
        return instance
