__author__ = 'brandonantonelli'
from kitbuilder.kitbuilder_v1.models import Sample

sample = Sample.objects.get(pk=1)
print sample.s3_preview_url