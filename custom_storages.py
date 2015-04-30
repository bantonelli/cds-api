STATICFILES_LOCATION = 'assets'
MEDIAFILES_LOCATION = 'media'

from require_s3.storage import OptimizedCachedStaticFilesStorage
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(OptimizedCachedStaticFilesStorage):
    location = STATICFILES_LOCATION


class MediaStorage(S3BotoStorage):
    location = MEDIAFILES_LOCATION