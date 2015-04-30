STATICFILES_LOCATION = 'assets'

from require_s3.storage import OptimizedCachedStaticFilesStorage
from storages.backends.s3boto import S3BotoStorage

class StaticStorage(S3BotoStorage):
    location = STATICFILES_LOCATION