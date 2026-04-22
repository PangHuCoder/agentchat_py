"""
向量存储服务 - 使用LangChain Milvus VectorStore
"""
from langchain_milvus import Milvus
from langchain.schema import Document
from typing import List, Optional
from pymilvus import utility, connections


class VectorStoreService:
    """使用LangChain的Milvus VectorStore"""
    
    def __init__(self, milvus_uri: str, embedding_service):
        """
        初始化向量存储服务
        
        Args:
            milvus_uri: Milvus连接URI
            embedding_service: 向量化服务实例
        """
        self.milvus_uri = milvus_uri
        self.embedding_service = embedding_service
    
    def create_collection(self, knowledge_id: int) -> Milvus:
        """
        创建知识库对应的Milvus collection
        
        Args:
            knowledge_id: 知识库ID
            
        Returns:
            Milvus VectorStore实例
        """
        collection_name = f"knowledge_{knowledge_id}"
        
        vector_store = Milvus(
            embedding_function=self.embedding_service.embeddings,
            collection_name=collection_name,
            connection_args={"uri": self.milvus_uri},
            auto_id=False,  # 使用自定义ID（slice_id）
            primary_field="id",
            vector_field="vector",
            text_field="content"
        )
        
        return vector_store
    
    def add_documents(
        self, 
        vector_store: Milvus, 
        texts: List[str], 
        metadatas: List[dict],
        ids: List[str]
    ):
        """
        添加文档到向量存储
        
        Args:
            vector_store: Milvus VectorStore实例
            texts: 文本列表
            metadatas: 元数据列表
            ids: ID列表
        """
        documents = [
            Document(page_content=text, metadata=metadata)
            for text, metadata in zip(texts, metadatas)
        ]
        vector_store.add_documents(documents=documents, ids=ids)
    
    def delete_by_document_id(self, vector_store: Milvus, document_id: int):
        """
        删除指定文档的所有向量
        
        Args:
            vector_store: Milvus VectorStore实例
            document_id: 文档ID
        """
        vector_store.delete(expr=f"document_id == {document_id}")
    
    def drop_collection(self, knowledge_id: int):
        """
        删除collection
        
        Args:
            knowledge_id: 知识库ID
        """
        collection_name = f"knowledge_{knowledge_id}"
        connections.connect(uri=self.milvus_uri)
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
