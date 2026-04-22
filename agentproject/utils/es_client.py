"""
Elasticsearch客户端工具
"""
from elasticsearch import Elasticsearch
from typing import Optional
from agentproject.settings import app_settings


class ESClient:
    """Elasticsearch客户端封装"""
    
    def __init__(self):
        """初始化ES客户端"""
        es_config = app_settings.elasticsearch
        self.client = Elasticsearch(
            hosts=[es_config.get('url', 'http://localhost:9200')],
            api_key=es_config.get('api_key'),
            verify_certs=False
        )
    
    def create_index(self, index_name: str, body: dict):
        """
        创建索引
        
        Args:
            index_name: 索引名称
            body: 索引配置（settings和mappings）
        """
        if not self.client.indices.exists(index=index_name):
            self.client.indices.create(index=index_name, body=body)
    
    def delete_index(self, index_name: str):
        """
        删除索引
        
        Args:
            index_name: 索引名称
        """
        if self.client.indices.exists(index=index_name):
            self.client.indices.delete(index=index_name)
    
    def index_document(self, index_name: str, doc_id: int, document: dict):
        """
        索引文档
        
        Args:
            index_name: 索引名称
            doc_id: 文档ID
            document: 文档内容
        """
        self.client.index(index=index_name, id=doc_id, document=document)
    
    def bulk_index(self, index_name: str, documents: list):
        """
        批量索引文档
        
        Args:
            index_name: 索引名称
            documents: 文档列表，每个文档包含id和内容
        """
        from elasticsearch.helpers import bulk
        
        actions = [
            {
                "_index": index_name,
                "_id": doc["id"],
                "_source": doc["source"]
            }
            for doc in documents
        ]
        bulk(self.client, actions)
    
    def search(self, index_name: str, query: dict, size: int = 10):
        """
        搜索文档
        
        Args:
            index_name: 索引名称
            query: 查询条件
            size: 返回结果数量
            
        Returns:
            搜索结果
        """
        return self.client.search(index=index_name, body=query, size=size)
    
    def delete_by_query(self, index_name: str, query: dict):
        """
        根据查询条件删除文档
        
        Args:
            index_name: 索引名称
            query: 查询条件
        """
        self.client.delete_by_query(index=index_name, body=query)
