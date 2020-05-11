import boto3
import uuid
from config import Ivysaur


class UploadHelper(object):

    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=Ivysaur.Config.S3_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Ivysaur.Config.S3_AWS_SECRET_ACCESS_KEY
        )
        self.s3_image_bucket = Ivysaur.Config.S3_IMAGE_BUCKET
        self.s3_video_bucket = Ivysaur.Config.S3_VIDEO_BUCKET
        self.s3_image_cloudfront = Ivysaur.Config.S3_IMAGE_CLOUDFRONT
        self.s3_video_cloudfront = Ivysaur.Config.S3_VIDEO_CLOUDFRONT
        self.expire = 3600

    def generate_image_upload_params(self, file_name):
        unique_filename = str(uuid.uuid4()) + '-' + file_name
        presigned_post = self.s3.generate_presigned_post(
            Bucket=self.s3_image_bucket,
            Key=unique_filename,
            ExpiresIn=self.expire
        )
        presigned_post['bucket_name'] = self.s3_image_bucket
        return presigned_post

    def generate_video_upload_params(self, file_name):
        unique_filename = str(uuid.uuid4()) + '-' + file_name
        presigned_post = self.s3.generate_presigned_post(
            Bucket=self.s3_video_bucket,
            Key=unique_filename,
            ExpiresIn=self.expire
        )
        presigned_post['bucket_name'] = self.s3_video_bucket
        return presigned_post
