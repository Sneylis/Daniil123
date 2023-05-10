from django.contrib import admin
from .models import *
# Register your models here.

class catInLines(admin.StackedInline):
    model = Category
    extra = 3

class GroupAdmin(admin.ModelAdmin):
    fields = ['group']
    inlines = [catInLines]

admin.site.register(Group,GroupAdmin)
admin.site.register(Unit)
admin.site.register(Backet)