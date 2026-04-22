"""
Milvus客户端工具
"""
from pymilvus import connections, utility, Collection
from typing import Optional
from agentproject.settings import app_settings


class MilvusClient:
    """Milvus客户端封装"""
    
    def __init__(self):
        """初始化Milvus连接"""
        milvus_config = app_settings.milvus
        self.host = milvus_config.get('host', 'localhost')
        self.port = milvus_config.get('port', 19530)
        self.user = milvus_config.get('user', 'root')
        self.password = milvus_config.get('password', 'Milvus')
        
        # 建立连接
        connections.connect(
            alias="default",
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password
        )
    
    def has_collection(self, collection_name: str) -> bool:
        """
        检查collection是否存在
        
        Args:
            collection_name: collection名称
            
        Returns:
            是否存在
        """
        return utility.has_collection(collection_name)
    
    def drop_collection(self, collection_name: str):
        """
        删除collection
        
        Args:
            collection_name: collection名称
        """
        if self.has_collection(collection_name):
            utility.drop_collection(collection_name)
    
    def get_collection(self, collection_name: str) -> Optional[Collection]:
        """
        获取collection实例
        
        Args:
            collection_name: collection名称
            
        Returns:
            Collection实例，如果不存在返回None
        """
        if self.has_collection(collection_name):
            return Collection(collection_name)
        return None
    
    def load_collection(self, collection_name: str):
        """
        加载collection到内存
        
        Args:
            collection_name: collection名称
        """
        collection = self.get_collection(collection_name)
        if collection:
            collection.load()
    
    def release_collection(self, collection_name: str):
        """
        从内存释放collection
        
        Args:
            collection_name: collection名称
        """
        collection = self.get_collection(collection_name)
        if collection:
            collection.release()
