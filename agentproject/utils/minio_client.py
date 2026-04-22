"""
MinIO 客户端工具类
"""
from minio import Minio
from minio.error import S3Error
from loguru import logger
import tempfile
import os
from typing import Optional
from agentproject.settings import app_settings


class MinioClient:
    """MinIO 客户端"""
    
    def __init__(self):
        """初始化 MinIO 客户端"""
        self.client = None
        self.bucket_name = None
    
    def initialize(self):
        """初始化连接"""
        try:
            self.client = Minio(
                endpoint=app_settings.minio.endpoint,
                access_key=app_settings.minio.access_key,
                secret_key=app_settings.minio.secret_key,
                secure=app_settings.minio.secure
            )
            self.bucket_name = app_settings.minio.bucket_name
            
            # 确保 bucket 存在
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created bucket: {self.bucket_name}")
            
            logger.info("MinIO client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MinIO client: {e}")
            raise
    
    async def download_file(self, object_name: str) -> str:
        """
        从 MinIO 下载文件到临时目录
        :param object_name: 对象名称（文件路径）
        :return: 临时文件路径
        """
        try:
            # 创建临时文件
            suffix = os.path.splitext(object_name)[1]
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            temp_file_path = temp_file.name
            temp_file.close()
            
            # 下载文件
            self.client.fget_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                file_path=temp_file_path
            )
            
            logger.info(f"Downloaded file from MinIO: {object_name} -> {temp_file_path}")
            return temp_file_path
            
        except S3Error as e:
            logger.error(f"Failed to download file from MinIO: {e}")
            raise
    
    async def upload_file(self, file_path: str, object_name: str) -> str:
        """
        上传文件到 MinIO
        :param file_path: 本地文件路径
        :param object_name: 对象名称（存储路径）
        :return: 对象名称
        """
        try:
            self.client.fput_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                file_path=file_path
            )
            
            logger.info(f"Uploaded file to MinIO: {file_path} -> {object_name}")
            return object_name
            
        except S3Error as e:
            logger.error(f"Failed to upload file to MinIO: {e}")
            raise
    
    async def delete_file(self, object_name: str):
        """
        删除 MinIO 中的文件
        :param object_name: 对象名称
        """
        try:
            self.client.remove_object(
                bucket_name=self.bucket_name,
                object_name=object_name
            )
            logger.info(f"Deleted file from MinIO: {object_name}")
        except S3Error as e:
            logger.error(f"Failed to delete file from MinIO: {e}")
            raise
    
    async def cleanup_temp_file(self, temp_file_path: str):
        """
        清理临时文件
        :param temp_file_path: 临时文件路径
        """
        try:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                logger.debug(f"Cleaned up temp file: {temp_file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup temp file: {e}")


# 全局 MinIO 客户端实例
minio_client = MinioClient()
