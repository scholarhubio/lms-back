from django.contrib import admin, messages
from django.http.request import HttpRequest

from django.db import models as django_models
from courses import models
from django.forms import Textarea
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


class MyNestedModelAdmin(NestedModelAdmin):
    formfield_overrides = {
        django_models.TextField: {
            "widget": admin.widgets.AdminTextareaWidget(
                attrs={"rows": 2, "cols": 80, "style": "height: 4em; width: 30em;"}
            )
        }
    }


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


class AnswerInline(MyNestedTabularAdmin):
    # input forms: text, is_correct, manual
    classes = ("collapse", "wide")
    verbose_name = "AnswerInline"  # note
    model = models.Answer
    extra = 0
    formfield_overrides = {
        django_models.TextField: {
            "widget": Textarea()
        }  # optional, set Textarea attributes `attrs={'rows':2, 'cols':8}`
    }


class TaskItemInline(MyNestedTabularAdmin):
    model = models.TaskItem
    verbose_name = "Item"
    extra = 1


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


@admin.register(models.Module)
class ModuleAdmin(MyNestedModelAdmin):
    list_display = ("title", "slug")
    readonly_fields = ("slug",)
    inlines = (UnitInLine,)

    fields = (("title", "slug"),)
