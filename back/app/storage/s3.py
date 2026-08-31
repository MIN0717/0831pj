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

        # Access Key가 존재할 때만 직접 Credential 사용
        # EC2 IAM Role을 사용하는 경우에는 자동으로 AWS Credential을 탐색함
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

        self.client = boto3.client(
            **client_options
        )

        self.bucket = settings.AWS_S3_BUCKET_NAME


    # ==========================================
    # CREATE
    # ==========================================

    def upload_file(
        self,
        file: BinaryIO,
        key: str,
        content_type: str | None = None,
    ) -> str:
        """
        파일 객체를 S3에 업로드한다.

        예:
        images/kimchi/123.jpg
        """

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


    def upload_local_file(
        self,
        file_path: str | Path,
        key: str,
    ) -> str:
        """
        로컬 파일을 S3에 업로드한다.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"파일을 찾을 수 없습니다: {path}"
            )

        try:
            self.client.upload_file(
                Filename=str(path),
                Bucket=self.bucket,
                Key=key,
            )

            return key

        except ClientError as e:
            raise RuntimeError(
                f"S3 업로드 실패: {e}"
            ) from e


    # ==========================================
    # READ
    # ==========================================

    def get_file(
        self,
        key: str,
    ) -> bytes:
        """
        S3 파일을 bytes 형태로 가져온다.
        """

        try:
            response = self.client.get_object(
                Bucket=self.bucket,
                Key=key,
            )

            return response["Body"].read()

        except ClientError as e:
            error_code = e.response.get(
                "Error",
                {},
            ).get(
                "Code",
                "",
            )

            if error_code in {
                "NoSuchKey",
                "404",
                "NotFound",
            }:
                raise FileNotFoundError(
                    f"S3 파일을 찾을 수 없습니다: {key}"
                ) from e

            raise RuntimeError(
                f"S3 파일 조회 실패: {e}"
            ) from e


    def list_files(
        self,
        prefix: str = "",
    ) -> list[str]:
        """
        특정 경로(prefix)의 파일 목록을 가져온다.

        예:
        prefix="images/김치찌개/"
        """

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


    def exists(
        self,
        key: str,
    ) -> bool:
        """
        파일 존재 여부를 확인한다.
        """

        try:
            self.client.head_object(
                Bucket=self.bucket,
                Key=key,
            )

            return True

        except ClientError as e:
            error_code = e.response.get(
                "Error",
                {},
            ).get(
                "Code",
                "",
            )

            if error_code in {
                "404",
                "NoSuchKey",
                "NotFound",
            }:
                return False

            raise RuntimeError(
                f"S3 파일 확인 실패: {e}"
            ) from e


    def generate_presigned_url(
        self,
        key: str,
        expires_in: int = 3600,
    ) -> str:
        """
        S3 파일에 접근할 수 있는 임시 URL을 생성한다.

        기본 만료시간: 1시간
        """

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
                f"S3 Presigned URL 생성 실패: {e}"
            ) from e


    # ==========================================
    # UPDATE
    # ==========================================

    def update_file(
        self,
        file: BinaryIO,
        key: str,
        content_type: str | None = None,
    ) -> str:
        """
        기존 key에 새 파일을 업로드한다.

        S3에서는 같은 key로 업로드하면
        기존 객체가 덮어써진다.
        """

        return self.upload_file(
            file=file,
            key=key,
            content_type=content_type,
        )


    # ==========================================
    # DELETE
    # ==========================================

    def delete_file(
        self,
        key: str,
    ) -> bool:
        """
        S3 파일을 삭제한다.
        """

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