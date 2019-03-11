from django.contrib import admin
from .models import Subject, Module, Topic, Quiz

# Register your models here.
admin.site.register(Subject)

class TopicInline(admin.TabularInline):
	model = Topic

class ModuleAdmin(admin.ModelAdmin):
	inlines = [
        TopicInline
	]
admin.site.register(Module, ModuleAdmin)

admin.site.register(Quiz)