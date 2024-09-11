from django.db.models.signals import pre_save
from django.dispatch import receiver
from courses.models.task import Task
from courses.models.course import CourseModule
from courses.models.module import Unit


@receiver(pre_save, sender=Task)
def order_task(sender, instance: Task, *args, **kwargs):
    last_obj = Task.objects.filter(unit=instance.unit).order_by('unit__order', 'parent', 'order').last()
    if not last_obj:
        instance.order = 1
        return instance 
    last_order = last_obj.order
    if instance.order:
        instance.order = last_order + 1
    else:
        instance.order = 1
    return instance


@receiver(pre_save, sender=CourseModule)
def order_module(sender, instance: CourseModule, *args, **kwargs):
    last_obj = CourseModule.objects.filter(course=instance.course).order_by('course', 'module', 'order').last()
    if not last_obj:
        instance.order = 1
        return instance 
    last_order = last_obj.order
    if instance.order:
        instance.order = last_order + 1
    else:
        instance.order = 1
    return instance


@receiver(pre_save, sender=Unit)
def order_unit(sender, instance: Unit, *args, **kwargs):
    last_obj = Unit.objects.filter(module=instance.module).order_by('module', 'order').last()
    if not last_obj:
        instance.order = 1
        return instance 
    last_order = last_obj.order
    if instance.order:
        instance.order = last_order + 1
    else:
        instance.order = 1
    return instance
