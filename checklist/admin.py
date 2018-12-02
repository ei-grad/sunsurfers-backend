from django.contrib import admin

from admin_ordering.admin import OrderableAdmin

from checklist import models


admin.site.register(models.TelegramBot)


class ItemsInline(OrderableAdmin, admin.StackedInline):
    model = models.Item
    fk_name = 'checklist'
    ordering_field = 'ordernum'


class ChecklistAdmin(admin.ModelAdmin):
    inlines = [ItemsInline]


admin.site.register(models.Checklist, ChecklistAdmin)
