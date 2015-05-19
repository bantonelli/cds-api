class ListFilterMixin(object):

    def patch(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        model = self.serializer_class.Meta.model
        if self.request.method == 'PATCH':
            request_items = self.request.data.get('request_items')
            if request_items is not None:
                return model.objects.filter(id__in=request_items)
            else:
                return model.objects.all()
        else:
            return model.objects.all()