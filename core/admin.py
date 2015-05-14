from django.contrib.sites.models import Site

__author__ = 'yuri'

from django.contrib import admin
from models import *

class Projectinlines(admin.TabularInline):
    model = Project
    extra = 0
    exclude = ['created_by']

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [Projectinlines,]
    list_display = ['name','created_by','created_at',]
    list_filter = ['name','created_by','created_at',]
    search_fields = ['name','created_by','created_at',]
    exclude = ['created_by']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.created_by = request.user
            instance.save()
        formset.save_m2m()


class Historyinlines(admin.TabularInline):
    model = History
    extra = 0
    exclude = ['created_by']

class ProjectAdmin(admin.ModelAdmin):
    inlines = [Historyinlines,]
    list_display = ['name','organization','created_by','created_at',]
    list_filter = ['name','organization','created_by','created_at',]
    search_fields = ['name','organization','created_by','created_at',]
    exclude = ['created_by']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.created_by = request.user
            instance.save()
        formset.save_m2m()

class Taskinlines(admin.TabularInline):
    model = Task
    extra = 0
    exclude = ['created_by']

class HistoryAdmin(admin.ModelAdmin):
    inlines = [Taskinlines,]
    list_display = ['name','project', 'sprint','weight','priority','estimate','created_by','created_at',]
    list_filter = ['project','created_by','created_at','sprint']
    exclude = ['created_by']
    ordering = ['sprint','priority']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.created_by = request.user
            instance.save()
        formset.save_m2m()

    def estimate(self, obj):
        tasks = Task.objects.filter(history__pk=obj.pk)
        print tasks
        total = 0
        if tasks:
            for task in tasks:
                try:
                    total = total + int(task.estimate)
                except ValueError:
                    pass
        return total
    estimate.short_description = "Estimate"

# class SprintTaskInLine(admin.TabularInline):
#     model = SprintTask
#     extra = 0
#     exclude = ['created_by']


class SprintAdmin(admin.ModelAdmin):
    # inlines = [SprintTaskInLine,]
    list_display = ['name','created_at','end_at','created_by']
    list_filter = ['created_at','end_at','created_by']
    exclude = ['created_by']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.created_by = request.user
            instance.save()
        formset.save_m2m()

class TaskAdmin(admin.ModelAdmin):
    list_display = ['name','history','created_at','completed_at','created_by']
    list_filter = ['created_at','created_by']
    search_fields = ['name','history__name','history__description','created_at','created_by']
    exclude = ['created_by']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

class WorkHourAdmin(admin.ModelAdmin):
    list_display = ['task','user','day','time']
    list_filter = ['user','day']
    search_fields = ['name','task__history__name','task__history__description','created_at','created_by']
    date_hierarchy = 'day'
    exclude = ['user']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Sprint, SprintAdmin)
#admin.site.register(SprintTask)
admin.site.register(WorkHour, WorkHourAdmin)
admin.site.unregister(Site)
