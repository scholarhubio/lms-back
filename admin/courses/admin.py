from django.contrib import admin
from django.db import models as django_models
from courses import models
from django.forms import forms, Textarea
from nested_admin import (
    NestedModelAdmin,
    NestedStackedInline,
)


class MyNestedModelAdmin(NestedModelAdmin):
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


class MyNestedStackedInline(NestedStackedInline):
    """
    Класс для настройки вложенного инлайн-администрирования модели с использованием 
    NestedStackedInline и переопределением виджета текстового поля.
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


@admin.register(models.Course)
class CourseAdmin(NestedModelAdmin):
    """
    Класс для настройки административного интерфейса модели Course.
    Использует NestedModelAdmin для поддержки вложенных моделей.

    Атрибуты:
        list_display (tuple): Поля, отображаемые в списке объектов.
        readonly_fields (tuple): Поля, доступные только для чтения.
    """
    
    list_display = ('title', 'lessons_per_day')
    readonly_fields = ('slug',)


class AnswerInline(NestedStackedInline):
    """
    Класс для настройки инлайн-администрирования модели Answer с использованием NestedStackedInline.

    Атрибуты:
        model (Model): Модель, используемая для инлайн-администрирования.
        extra (int): Количество дополнительных пустых форм, отображаемых в админке (по умолчанию 0).
        formfield_overrides (dict): Переопределение виджета для текстовых полей.
    """

    model = models.Answer 
    extra = 0 
    
    # Переопределение виджета для полей TextField.
    formfield_overrides = {
        django_models.TextField: {
            'widget': Textarea()  # Настройка атрибутов текстовой области (опционально).
        }
    }


class TaskInlineSelf(NestedStackedInline):
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


class TaskInline(NestedStackedInline):
    """
    Класс для настройки инлайн-администрирования модели Task с использованием NestedStackedInline.

    Атрибуты:
        model (Model): Модель, используемая для инлайн-администрирования.
        extra (int): Количество дополнительных пустых форм, отображаемых в админке (по умолчанию 0).
        inlines (list): Список вложенных инлайн-классов, которые будут отображаться вместе с основной моделью.
    """

    model = models.Task 
    extra = 0  
    inlines = [AnswerInline, TaskInlineSelf]



class UnitItemInline(MyNestedStackedInline):
    """
    Класс для настройки инлайн-администрирования модели UnitItem с использованием 
    пользовательского класса MyNestedStackedInline.

    Атрибуты:
        model (Model): Модель, используемая для инлайн-администрирования.
        extra (int): Количество дополнительных пустых форм, отображаемых в админке (по умолчанию 0).
    """

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

    model = models.Unit
    extra = 0  
    inlines = [TaskInline, UnitItemInline]  


@admin.register(models.Module)
class ModuleAdmin(MyNestedModelAdmin):
    """
    Класс для настройки административного интерфейса модели Module с использованием 
    пользовательского класса MyNestedModelAdmin.

    Атрибуты:
        list_display (tuple): Поля, отображаемые в списке объектов в админке.
        inlines (list): Список вложенных инлайн-классов, отображаемых вместе с основной моделью.
    """

    list_display = ('title',) 
    inlines = [UnitInline]