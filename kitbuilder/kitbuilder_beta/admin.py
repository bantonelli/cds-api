from django.contrib import admin
from models import *


class TagInline(admin.TabularInline):
    model = Kit.tags.through


class KitAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('tags', 'on_sale', 'active')
    # inlines = [
    #     TagInline,
    # ]
    # exclude = ('tags',)


# class TagAdmin(admin.ModelAdmin):
#     inlines = [
#         TagInline,
#     ]


class SampleAdmin(admin.ModelAdmin):
    list_display = ('name', 'kit', 'type')


admin.site.register(Price)
admin.site.register(Sale)
admin.site.register(Tag)
admin.site.register(KitDescription)
admin.site.register(Kit, KitAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(CustomKit)
