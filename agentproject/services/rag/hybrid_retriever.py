"""
混合检索服务 - 使用LangChain EnsembleRetriever
"""
from langchain.retrievers import EnsembleRetriever
from langchain_milvus import Milvus
from langchain_community.retrievers import ElasticsearchRetriever
from typing import List


class HybridRetrieverService:
    """使用LangChain的EnsembleRetriever实现混合检索"""
    
    def __init__(
        self,
        milvus_uri: str,
        es_url: str,
        embedding_service
    ):
        """
        初始化混合检索服务
        
        Args:
            milvus_uri: Milvus连接URI
            es_url: Elasticsearch连接URL
            embedding_service: 向量化服务实例
        """
        self.milvus_uri = milvus_uri
        self.es_url = es_url
        self.embedding_service = embedding_service
    
    def create_retriever(self, knowledge_id: int, top_k: int = 5) -> EnsembleRetriever:
        """
        创建混合检索器
        
        Args:
            knowledge_id: 知识库ID
            top_k: 返回结果数量
            
        Returns:
            EnsembleRetriever实例
        """
        collection_name = f"knowledge_{knowledge_id}"
        index_name = f"knowledge_slice_{knowledge_id}"
        
        # 创建Milvus向量检索器
        vector_store = Milvus(
            embedding_function=self.embedding_service.embeddings,
            collection_name=collection_name,
            connection_args={"uri": self.milvus_uri}
        )
        vector_retriever = vector_store.as_retriever(
            search_kwargs={"k": top_k * 2}
        )
        
        # 创建Elasticsearch全文检索器
        es_retriever = ElasticsearchRetriever(
            es_url=self.es_url,
            index_name=index_name,
            body_func=lambda query: {
                "query": {
                    "match": {
                        "content": {
                            "query": query,
                            "analyzer": "ik_smart"
                        }
                    }
                },
                "size": top_k * 2
            }
        )
        
        # 创建混合检索器：0.6 * vector + 0.4 * fulltext
        ensemble_retriever = EnsembleRetriever(
            retrievers=[vector_retriever, es_retriever],
            weights=[0.6, 0.4]
        )
        
        return ensemble_retriever
    
    def search(
        self, 
        knowledge_id: int, 
        query: str, 
        top_k: int = 5
    ) -> List[dict]:
        """
        执行混合检索
        
        Args:
            knowledge_id: 知识库ID
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            检索结果列表
        """
        retriever = self.create_retriever(knowledge_id, top_k)
        
        # 执行检索
        results = retriever.get_relevant_documents(query)
        
        # 转换为响应格式
        search_results = []
        for i, doc in enumerate(results[:top_k]):
            search_results.append({
                "slice_id": doc.metadata.get("slice_id"),
                "document_id": doc.metadata.get("document_id"),
                "content": doc.page_content,
                "vector_score": doc.metadata.get("vector_score", 0.0),
                "fulltext_score": doc.metadata.get("fulltext_score", 0.0),
                "final_score": doc.metadata.get("score", 0.0),
                "rank": i + 1
            })
        
        # 过滤低分结果
        search_results = [r for r in search_results if r["final_score"] >= 0.3]
        
        return search_results
