from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage): #임의로 정한 이름 -> amazon 파일관리
    location = 'media'
    bucket_name = 'images.innorev.site'
    custom_domain = 'images.innorev.site'
    file_overwrite = False