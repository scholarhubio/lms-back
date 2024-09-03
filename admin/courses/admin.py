from django.contrib import admin
from django.db import models as django_models
from courses import models
from django.forms import forms, Textarea
from nested_admin import (
    NestedModelAdmin,
    NestedStackedInline,
    NestedTabularInline,
)


class MyNestedModelAdmin(NestedModelAdmin):
    formfield_overrides = {
        django_models.TextField: {
            'widget': admin.widgets.AdminTextareaWidget(
                attrs={
                    'rows':2,
                    'cols': 80,
                    'style':'height: 4em; width: 30em;'
                }
            )
        }
    }   


class MyNestedStackedInline(NestedStackedInline):
    formfield_overrides = {
        django_models.TextField: {
            'widget': admin.widgets.AdminTextareaWidget(
                attrs={
                    'rows':2,
                    'cols': 80,
                    'style':'height: 4em; width: 30em;'
                }
            )
        }
    }


@admin.register(models.Course)
class CourseAdmin(NestedModelAdmin):
    list_display = ('title' ,'lessons_per_day',)
    readonly_fields = ('slug',)


class AnswerInline(NestedStackedInline):
    model = models.Answer
    extra = 0
    formfield_overrides = {
        django_models.TextField: {'widget': Textarea()} #optional, set Textarea attributes `attrs={'rows':2, 'cols':8}`
    }


class TaskInlineSelf(NestedStackedInline):
    model = models.Task
    verbose_name = "subtask"
    extra = 0


class TaskInline(NestedStackedInline):
    model = models.Task
    extra = 0
    inlines = [AnswerInline, TaskInlineSelf]


class UnitItemInline(MyNestedStackedInline):
    model = models.UnitItem
    extra = 0


class UnitInline(MyNestedStackedInline):
    model = models.Unit
    extra = 0
    inlines = [TaskInline, UnitItemInline,]


@admin.register(models.Module)
class ModuleAdmin(MyNestedModelAdmin):
    list_display = ('title',)
    inlines = [UnitInline,]
