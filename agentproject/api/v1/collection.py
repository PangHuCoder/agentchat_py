"""
Milvus Collection管理API端点
"""
from fastapi import APIRouter, HTTPException, Query
from agentproject.api.v1.models import OperationResponse
from agentproject.services.rag.embeddings import EmbeddingService
from agentproject.services.rag.vector_store import VectorStoreService
from agentproject.settings import app_settings

router = APIRouter(prefix="/collection", tags=["Collection管理"])

# 初始化服务
embedding_service = EmbeddingService()
milvus_uri = f"http://{app_settings.milvus.get('host', 'localhost')}:{app_settings.milvus.get('port', 19530)}"
vector_store_service = VectorStoreService(milvus_uri, embedding_service)


@router.post("/create", response_model=OperationResponse, summary="创建Collection")
async def create_collection(knowledge_id: int = Query(..., description="知识库ID")):
    """
    创建Milvus collection（使用LangChain Milvus）
    
    Args:
        knowledge_id: 知识库ID
        
    Returns:
        操作结果
        
    Raises:
        HTTPException: 创建失败
    """
    try:
        vector_store_service.create_collection(knowledge_id)
        return OperationResponse(
            success=True,
            message=f"Collection knowledge_{knowledge_id} 创建成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"创建Collection失败: {str(e)}"
        )


@router.delete("/{knowledge_id}", response_model=OperationResponse, summary="删除Collection")
async def drop_collection(knowledge_id: int):
    """
    删除Milvus collection
    
    Args:
        knowledge_id: 知识库ID
        
    Returns:
        操作结果
        
    Raises:
        HTTPException: 删除失败
    """
    try:
        vector_store_service.drop_collection(knowledge_id)
        return OperationResponse(
            success=True,
            message=f"Collection knowledge_{knowledge_id} 删除成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除Collection失败: {str(e)}"
        )
