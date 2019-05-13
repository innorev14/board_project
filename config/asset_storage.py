# pip install django-storages
# pip install boto3
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage): #임의로 정한 이름 -> amazon 파일관리
    # S3에서 location 에서 설정한 폴더에서 media관리
    location = ''
    bucket_name = 'images.innorev.site'
    custom_domain = 'images.innorev.site'
    file_overwrite = False