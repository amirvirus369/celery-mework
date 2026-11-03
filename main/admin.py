from django.contrib import admin
from main import models
from parler.admin import TranslatableAdmin,TranslatableTabularInline
# Register your models here.
@admin.register(models.Career_field)
class CareerFieldAdmin(TranslatableAdmin):
    list_display = ('name',)

@admin.register(models.Job)
class jobdAdmin(TranslatableAdmin):
    list_display = ('title',)


class exp_Admin(TranslatableTabularInline):
    model = models.Experience
    extra = 1

@admin.register(models.Resumeh_me)
class resumehAdmin(TranslatableAdmin):
    inlines = (exp_Admin,)