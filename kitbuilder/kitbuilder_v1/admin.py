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
admin.site.register(TemplateFollow)
admin.site.register(KitBuilderPurchase)


"""
The model Resource has a few methods that can be overridden:

- This will make the resource always create a new record when you import.
def get_instance(self, instance_loader, row):
    return False

- This is how you customize overwriting/updating records on an import
def save_instance(self, instance, real_dry_run):
    if not real_dry_run:
            try:
                obj = YourModel.objects.get(some_val=instance.some_val)
                # extra logic if object already exist
            except NFCTag.DoesNotExist:
                # create new object
                obj = YourModel(some_val=instance.some_val)
                obj.save()

- This example makes the import system simpler by not requiring an id column as it does now.
def before_import(self, dataset, dry_run):

    if dataset.headers:
        dataset.headers = [str(header).lower().strip() for header in dataset.headers]

        #if id column not in headers in your file
        if 'id' not in dataset.headers:
            dataset.headers.append('id')

"""