from django.contrib import admin
from models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class SampleResource(resources.ModelResource):

    class Meta:
        model = Sample


class SampleAdmin(ImportExportModelAdmin):
    resource_class = SampleResource
    list_display = ('name', 'vendor_kit', 'type')


class TagInline(admin.TabularInline):
    model = VendorKit.tags.through


class VendorKitAdmin(admin.ModelAdmin):
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


admin.site.register(Price)
admin.site.register(Sale)
admin.site.register(Tag)
admin.site.register(VendorKit, VendorKitAdmin)
admin.site.register(Vendor)
admin.site.register(Sample, SampleAdmin)
admin.site.register(KitBuilderTemplate)
admin.site.register(KitBuilderPurchase)
