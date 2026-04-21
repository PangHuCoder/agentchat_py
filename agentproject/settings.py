"""
应用配置管理
"""
import yaml
from loguru import logger
from types import SimpleNamespace
from pydantic import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""
    # 服务配置
    server: dict = {}
    # MySQL 配置
    mysql: dict = {}
    # Redis 配置
    redis: dict = {}
    # Elasticsearch 配置
    elasticsearch: dict = {}
    # Milvus 配置
    milvus: dict = {}
    # Embedding 配置
    embedding: dict = {}
    # MinIO 配置
    minio: dict = {}
    # 文档处理配置
    document: dict = {}
    # 检索配置
    retrieval: dict = {}
    # 日志配置
    logging: dict = {}
    class Config:
        arbitrary_types_allowed = True


# 全局配置实例
app_settings = Settings()


async def initialize_app_settings(file_path: str = None):
    """
    初始化应用配置
    :param file_path: 配置文件路径
    """
    global app_settings
    
    file_path = file_path or "agentproject/config.yaml"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if data is None:
                logger.error("YAML 文件解析为空")
                return
            
            # 将配置数据动态设置到 app_settings
            for key, value in data.items():
                if isinstance(value, dict):
                    # 将字典转换为 SimpleNamespace，支持点号访问
                    setattr(app_settings, key, SimpleNamespace(**value))
                else:
                    setattr(app_settings, key, value)
                logger.info(f"Loaded {key}: {value}")
                
    except Exception as e:
        logger.error(f"Yaml file loading error: {e}")


def get_settings() -> Settings:
    """获取配置实例"""
    return app_settings
