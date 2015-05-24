STATICFILES_LOCATION = 'assets'
MEDIAFILES_LOCATION = 'media'

from require_s3.storage import OptimizedCachedStaticFilesStorage
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(OptimizedCachedStaticFilesStorage):
    location = STATICFILES_LOCATION

    # Had to override this property to pass in the 'host' parameter and quiet error
    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connection_class(
                self.access_key, self.secret_key, host='s3.amazonaws.com',
                calling_format=self.calling_format)
        return self._connection


class MediaStorage(S3BotoStorage):
    location = MEDIAFILES_LOCATION