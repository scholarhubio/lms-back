from django.forms.models import BaseInlineFormSet
from nested_admin import NestedModelAdmin, NestedStackedInline
from django.db import models as django_models
from django.contrib import admin, messages
from django.http.request import HttpRequest


class BaseModelAdmin(admin.ModelAdmin):
    exclude = ('is_deleted',)
    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).filter(is_deleted=False)

    def delete_model(self, request, obj):
        """Soft delete the object by setting `is_deleted` to True instead of deleting."""
        obj.is_deleted = True
        obj.save()
        self.message_user(request, f"{obj} has been soft deleted.", level=messages.INFO)


class BaseStackedInline(admin.StackedInline):
    exclude = ('is_deleted',)
    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).filter(is_deleted=False)

    def delete_model(self, request, obj):
        """Soft delete the object by setting `is_deleted` to True instead of deleting."""
        obj.is_deleted = True
        obj.save()
        self.message_user(request, f"{obj} has been soft deleted.", level=messages.INFO)


class SoftDeleteInlineFormSet(BaseInlineFormSet):
    def delete_existing(self, obj, commit=True):
        """Override to perform a soft delete instead of an actual delete."""
        obj.is_deleted = True
        if commit:
            obj.save()  # Save the object to update the `is_deleted` flag


class MyNestedModelAdmin(NestedModelAdmin, BaseModelAdmin):
    """
    Класс для настройки администрирования вложенной модели с использованием 
    NestedModelAdmin и переопределением виджета текстового поля.
    """

    # Переопределение виджета для полей TextField.
    formfield_overrides = {
        django_models.TextField: {
            'widget': admin.widgets.AdminTextareaWidget(
                attrs={
                    'rows': 2,  # Установка количества строк в текстовой области.
                    'cols': 80,  # Установка количества колонок в текстовой области.
                    'style': 'height: 4em; width: 30em;'  # Задание стилей для текстовой области.
                }
            )
        }
    }


class MyNestedStackedInline(NestedStackedInline, BaseStackedInline):
    exclude = ('is_deleted',)
    """
    Класс для настройки вложенного инлайн-администрирования модели с использованием 
    NestedStackedInline и переопределением виджета текстового поля.
    """
    formset = SoftDeleteInlineFormSet
    # Переопределение виджета для полей TextField.
    formfield_overrides = {
        django_models.TextField: {
            'widget': admin.widgets.AdminTextareaWidget(
                attrs={
                    'rows': 2,  # Установка количества строк в текстовой области.
                    'cols': 80,  # Установка количества колонок в текстовой области.
                    'style': 'height: 4em; width: 30em;'  # Задание стилей для текстовой области.
                }
            )
        }
    }
