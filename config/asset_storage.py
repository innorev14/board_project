from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage): #임의로 정한 이름 -> amazon 파일관리
    location = 'media'
    file_overwrite = False