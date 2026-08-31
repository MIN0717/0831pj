from pathlib import Path
from typing import BinaryIO

import boto3
from botocore.exceptions import ClientError

from app.config import settings


class S3Storage:
    def __init__(self):
        client_options = {
            "service_name": "s3",
            "region_name": settings.AWS_REGION,
        }

        # 로컬에서 Access Key를 사용하는 경우
        if (
            settings.AWS_ACCESS_KEY_ID
            and settings.AWS_SECRET_ACCESS_KEY
        ):
            client_options["aws_access_key_id"] = (
                settings.AWS_ACCESS_KEY_ID
            )

            client_options["aws_secret_access_key"] = (
                settings.AWS_SECRET_ACCESS_KEY
            )

        # EC2에서는 Access Key가 없어도
        # IAM Role을 자동으로 사용
        self.client = boto3.client(
            **client_options
        )

        self.bucket = settings.S3_BUCKET_NAME


    # CREATE
    def upload_file(
        self,
        file: BinaryIO,
        key: str,
        content_type: str | None = None,
    ) -> str:

        extra_args = {}

        if content_type:
            extra_args["ContentType"] = content_type

        try:
            self.client.upload_fileobj(
                Fileobj=file,
                Bucket=self.bucket,
                Key=key,
                ExtraArgs=extra_args,
            )

            return key

        except ClientError as e:
            raise RuntimeError(
                f"S3 업로드 실패: {e}"
            ) from e


    # READ
    def get_file(
        self,
        key: str,
    ) -> bytes:

        try:
            response = self.client.get_object(
                Bucket=self.bucket,
                Key=key,
            )

            return response["Body"].read()

        except ClientError as e:
            raise RuntimeError(
                f"S3 파일 조회 실패: {e}"
            ) from e


    def list_files(
        self,
        prefix: str = "",
    ) -> list[str]:

        keys = []

        try:
            paginator = self.client.get_paginator(
                "list_objects_v2"
            )

            pages = paginator.paginate(
                Bucket=self.bucket,
                Prefix=prefix,
            )

            for page in pages:
                for item in page.get(
                    "Contents",
                    [],
                ):
                    keys.append(
                        item["Key"]
                    )

            return keys

        except ClientError as e:
            raise RuntimeError(
                f"S3 목록 조회 실패: {e}"
            ) from e


    def generate_presigned_url(
        self,
        key: str,
        expires_in: int = 3600,
    ) -> str:

        try:
            return self.client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": self.bucket,
                    "Key": key,
                },
                ExpiresIn=expires_in,
            )

        except ClientError as e:
            raise RuntimeError(
                f"S3 URL 생성 실패: {e}"
            ) from e


    # UPDATE
    def update_file(
        self,
        file: BinaryIO,
        key: str,
        content_type: str | None = None,
    ) -> str:

        return self.upload_file(
            file=file,
            key=key,
            content_type=content_type,
        )


    # DELETE
    def delete_file(
        self,
        key: str,
    ) -> bool:

        try:
            self.client.delete_object(
                Bucket=self.bucket,
                Key=key,
            )

            return True

        except ClientError as e:
            raise RuntimeError(
                f"S3 삭제 실패: {e}"
            ) from e


s3_storage = S3Storage()