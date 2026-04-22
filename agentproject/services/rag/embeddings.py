"""
向量化服务 - 使用LangChain HuggingFaceEmbeddings封装bge-small-zh-v1.5
"""
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List


class EmbeddingService:
    """使用LangChain的HuggingFaceEmbeddings封装bge-small-zh-v1.5"""
    
    def __init__(self, model_name: str = "BAAI/bge-small-zh-v1.5", device: str = "cpu"):
        """
        初始化向量化服务
        
        Args:
            model_name: 模型名称，默认为bge-small-zh-v1.5
            device: 运行设备，默认为cpu
        """
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': device},
            encode_kwargs={'normalize_embeddings': True}
        )
    
    def embed_query(self, text: str) -> List[float]:
        """
        生成查询向量（512维）
        
        Args:
            text: 查询文本
            
        Returns:
            512维向量
        """
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        批量生成文档向量（512维）
        
        Args:
            texts: 文档文本列表
            
        Returns:
            512维向量列表
        """
        return self.embeddings.embed_documents(texts)
