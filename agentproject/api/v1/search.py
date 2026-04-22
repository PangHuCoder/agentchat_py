"""
混合检索API端点
"""
from fastapi import APIRouter, HTTPException
from agentproject.api.v1.models import SearchRequest, SearchResponse
from agentproject.services.rag.embeddings import EmbeddingService
from agentproject.services.rag.hybrid_retriever import HybridRetrieverService
from agentproject.settings import app_settings

router = APIRouter(prefix="/search", tags=["混合检索"])

# 初始化服务
embedding_service = EmbeddingService()
milvus_uri = f"http://{app_settings.milvus.get('host', 'localhost')}:{app_settings.milvus.get('port', 19530)}"
es_url = app_settings.elasticsearch.get('url', 'http://localhost:9200')
hybrid_retriever_service = HybridRetrieverService(milvus_uri, es_url, embedding_service)


@router.post("", response_model=SearchResponse, summary="混合检索")
async def hybrid_search(request: SearchRequest):
    """
    混合检索（使用LangChain EnsembleRetriever）
    
    Args:
        request: 检索请求，包含知识库ID、查询文本和返回数量
        
    Returns:
        检索结果列表
        
    Raises:
        HTTPException: 检索失败
    """
    try:
        # 使用LangChain的混合检索器
        results = hybrid_retriever_service.search(
            knowledge_id=request.knowledge_id,
            query=request.query,
            top_k=request.top_k
        )
        
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"混合检索失败: {str(e)}"
        )
