from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticFileStorage(S3Boto3Storage):
    location = settings.STATIC_LOCATION
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):  #no use of media because i not used images in this project
    location = settings.PUBLIC_MEDIA_LOCATION
    file_overwrite = False
    default_acl = 'public-read'
