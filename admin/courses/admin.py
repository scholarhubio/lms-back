from django.contrib import admin, messages
<<<<<<< HEAD
from django.http.request import HttpRequest

=======
>>>>>>> main
from django.db import models as django_models
from django.http.request import HttpRequest
from courses import models
from django.forms import Textarea
<<<<<<< HEAD
from django import forms
from nested_admin import NestedModelAdmin, NestedTabularInline


admin.site.site_header = "Администрирование платформы Scholar"
admin.site.site_title = "Администрирование платформы Scholar"


class MyNestedTabularAdmin(NestedTabularInline):
    formfield_overrides = {
        django_models.TextField: {
            "widget": admin.widgets.AdminTextareaWidget(
                attrs={"rows": 2, "cols": 80, "style": "height: 4em; width: 30em;"}
            )
        }
    }
=======
from nested_admin import (
    NestedModelAdmin,
    NestedStackedInline,
)
from django import forms
from courses.models import Course, CourseModule, Module, UserAnswer, UserTaskSession
from courses.models.result import UserModuleSession, UserUnitSession
from django.db import IntegrityError, transaction
from typing import Any

from django.forms.models import BaseInlineFormSet


class SoftDeleteInlineFormSet(BaseInlineFormSet):
    def delete_existing(self, obj, commit=True):
        """Override to perform a soft delete instead of an actual delete."""
        obj.is_deleted = True
        if commit:
            obj.save()  # Save the object to update the `is_deleted` flag
>>>>>>> main


class MyNestedModelAdmin(NestedModelAdmin):
    exclude = ('is_deleted',)
    """
    Класс для настройки администрирования вложенной модели с использованием 
    NestedModelAdmin и переопределением виджета текстового поля.
    """

    # Переопределение виджета для полей TextField.
    formfield_overrides = {
        django_models.TextField: {
<<<<<<< HEAD
            "widget": admin.widgets.AdminTextareaWidget(
                attrs={"rows": 2, "cols": 80, "style": "height: 4em; width: 30em;"}
=======
            'widget': admin.widgets.AdminTextareaWidget(
                attrs={
                    'rows': 2,  # Установка количества строк в текстовой области.
                    'cols': 80,  # Установка количества колонок в текстовой области.
                    'style': 'height: 4em; width: 30em;'  # Задание стилей для текстовой области.
                }
            )
        }
    }

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).filter(is_deleted=False)

    def delete_model(self, request, obj):
        """Soft delete the object by setting `is_deleted` to True instead of deleting."""
        obj.is_deleted = True
        obj.save()
        self.message_user(request, f"{obj} has been soft deleted.", level=messages.INFO)


class MyNestedStackedInline(NestedStackedInline):
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
>>>>>>> main
            )
        }
    }
    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).filter(is_deleted=False)

    def delete_model(self, request, obj):
        """Soft delete the object by setting `is_deleted` to True instead of deleting."""
        obj.is_deleted = True
        obj.save()
        # Optionally, show a message to the admin user
        self.message_user(request, f"{obj} has been soft deleted.", level=messages.INFO)


<<<<<<< HEAD
######################################################
# NEW INLINES
# AUTHOR: SULTANOV ASADBEK
######################################################
@admin.register(models.Course)
class CourseAdmin(NestedModelAdmin):
    list_display = (
        "title",
        "lessons_per_day",
    )

    readonly_fields = ("slug",)

    def view_students_link(self, obj):
        count = obj.person_set.count
=======
class AnswerInline(MyNestedStackedInline):
    """
    Класс для настройки инлайн-администрирования модели Answer с использованием NestedStackedInline.
>>>>>>> main

    Атрибуты:
        model (Model): Модель, используемая для инлайн-администрирования.
        extra (int): Количество дополнительных пустых форм, отображаемых в админке (по умолчанию 0).
        formfield_overrides (dict): Переопределение виджета для текстовых полей.
    """

<<<<<<< HEAD
class AnswerInline(MyNestedTabularAdmin):
    # input forms: text, is_correct, manual
    classes = ("collapse", "wide")
    verbose_name = "AnswerInline"  # note
=======
>>>>>>> main
    model = models.Answer
    extra = 0
    
    # Переопределение виджета для полей TextField.
    formfield_overrides = {
        django_models.TextField: {
<<<<<<< HEAD
            "widget": Textarea()
        }  # optional, set Textarea attributes `attrs={'rows':2, 'cols':8}`
    }


class TaskItemInline(MyNestedTabularAdmin):
=======
            'widget': Textarea()  # Настройка атрибутов текстовой области (опционально).
        }
    }


class TaskItemInline(MyNestedStackedInline):
>>>>>>> main
    model = models.TaskItem
    verbose_name = "Item"
    extra = 1


<<<<<<< HEAD
class TaskInlineSelf(MyNestedTabularAdmin):
    # input forms: title, slug, order, unit, type
    classes = ("collapse", "wide")
    verbose_name = "subtask"
    model = models.Task
    extra = 1
    readonly_fields = ("slug",)


class TaskInLine(MyNestedTabularAdmin):
    readonly_fields = ("slug",)
    exclude = ("parent", "is_deleted")
    classes = ("collapse", "wide")
    model = models.Task
    extra = 1
    inlines = (AnswerInline, TaskInlineSelf, TaskItemInline)


class UnitItemInline(MyNestedTabularAdmin):
    classes = ("collapse", "wide")
    model = models.UnitItem
    extra = 1
    readonly_fields = ("slug",)


class UnitInLine(MyNestedTabularAdmin):
    classes = ("collapse", "wide")
    readonly_fields = ("slug",)
    model = models.Unit
    extra = 1
    inlines = (TaskInLine, UnitItemInline)
=======
class TaskInlineSelf(MyNestedStackedInline):
    """
    Класс для настройки инлайн-администрирования модели Task в виде вложенной модели.

    Атрибуты:
        model (Model): Модель, используемая для инлайн-администрирования.
        verbose_name (str): Название для отображения инлайн-модели в административной панели.
        extra (int): Количество дополнительных пустых форм, отображаемых в админке (по умолчанию 0).
    """

    model = models.Task 
    verbose_name = "subtask" 
    extra = 0


class TaskInline(MyNestedStackedInline):
    readonly_fields = ['order',]
    exclude = ('parent', 'is_deleted')
    """
    Класс для настройки инлайн-администрирования модели Task с использованием NestedStackedInline.

    Атрибуты:
        model (Model): Модель, используемая для инлайн-администрирования.
        extra (int): Количество дополнительных пустых форм, отображаемых в админке (по умолчанию 0).
        inlines (list): Список вложенных инлайн-классов, которые будут отображаться вместе с основной моделью.
    """

    model = models.Task 
    extra = 0  
    inlines = [AnswerInline, TaskInlineSelf, TaskItemInline]

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(parent=None).order_by('parent', 'order')


class UnitItemInline(MyNestedStackedInline):
    """
    Класс для настройки инлайн-администрирования модели UnitItem с использованием 
    пользовательского класса MyNestedStackedInline.

    Атрибуты:
        model (Model): Модель, используемая для инлайн-администрирования.
        extra (int): Количество дополнительных пустых форм, отображаемых в админке (по умолчанию 0).
    """
    classes = ('collapse',)
    model = models.UnitItem  
    extra = 0  


class UnitInline(MyNestedStackedInline):
    """
    Класс для настройки инлайн-администрирования модели Unit с использованием
    пользовательского класса MyNestedStackedInline.

    Атрибуты:
        model (Model): Модель, используемая для инлайн-администрирования.
        extra (int): Количество дополнительных пустых форм, отображаемых в админке (по умолчанию 0).
        inlines (list): Список вложенных инлайн-классов, отображаемых вместе с основной моделью.
    """
    classes = ('collapse',)
    readonly_fields = ['order',]
    model = models.Unit
    extra = 0  
    inlines = [TaskInline, UnitItemInline]
>>>>>>> main


@admin.register(models.Module)
class ModuleAdmin(MyNestedModelAdmin):
<<<<<<< HEAD
    list_display = ("title", "slug")
    readonly_fields = ("slug",)
    inlines = (UnitInLine,)

    fields = (("title", "slug"),)
=======
    """
    Класс для настройки административного интерфейса модели Module с использованием 
    пользовательского класса MyNestedModelAdmin.

    Атрибуты:
        list_display (tuple): Поля, отображаемые в списке объектов в админке.
        inlines (list): Список вложенных инлайн-классов, отображаемых вместе с основной моделью.
    """

    list_display = ('title',) 
    inlines = [UnitInline]


class CourseModuleInlineForm(forms.ModelForm):
    class Meta:
        model = CourseModule
        fields = ['module', 'order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['module'].queryset = Module.objects.all().exclude(is_deleted=True)

    def save(self, commit=True):
        try:
            with transaction.atomic():
                return super().save(commit=commit)
        except IntegrityError as e:
            # Instead of raising an error, return None and let the admin handle it
            self.add_error(None, "This module order combination already exists.")
            return self.instance


class CourseModuleInline(MyNestedStackedInline):
    model = CourseModule
    form = CourseModuleInlineForm
    extra = 1
    fields = ['module', 'order']
    readonly_fields = ['order',]

    def get_queryset(self, request: HttpRequest):
        qs = super().get_queryset(request).order_by('order')
        return qs.filter(is_deleted=False)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        return formset

    def save_formset(self, request, form, formset, change):
        # Save formset and check for errors
        has_errors = False
        for form in formset.forms:
            if form.errors:
                has_errors = True

        if has_errors:
            # Display error message when errors are detected in the formset
            self.message_user(
                request,
                "An error occurred while saving. The module order combination already exists.",
                level=messages.ERROR,
            )
        else:
            formset.save_m2m()


@admin.register(Course)
class CourseAdmin(MyNestedModelAdmin):
    list_display = ('title', 'lessons_per_day', 'is_deleted')
    inlines = [CourseModuleInline]
    search_fields = ['title']
    ordering = ['title']

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except IntegrityError:
            self.message_user(
                request,
                "Error: Duplicate entry detected for course module order.",
                level=messages.ERROR
            )


@admin.register(UserTaskSession)
class UserTaskSessionAdmin(MyNestedModelAdmin):
    pass


@admin.register(UserAnswer)
class UserAnswerAdmin(MyNestedModelAdmin):
    list_display = ('session', 'user_id', 'is_correct',)


@admin.register(UserModuleSession)
class UserModuleSessionAdmin(MyNestedModelAdmin):
    list_display = ('module',)


@admin.register(UserUnitSession)
class UserUnitSessionAdmin(MyNestedModelAdmin):
    list_display = ('unit',)
>>>>>>> main
