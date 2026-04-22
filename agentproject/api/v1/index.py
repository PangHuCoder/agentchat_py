"""
Elasticsearch Index管理API端点
"""
from fastapi import APIRouter, HTTPException, Query
from agentproject.api.v1.models import OperationResponse
from agentproject.utils.es_client import ESClient
from agentproject.config.es_index import ESIndex

router = APIRouter(prefix="/index", tags=["Index管理"])

# 初始化服务
es_client = ESClient()


@router.post("/create", response_model=OperationResponse, summary="创建Index")
async def create_index(knowledge_id: int = Query(..., description="知识库ID")):
    """
    创建Elasticsearch index
    
    Args:
        knowledge_id: 知识库ID
        
    Returns:
        操作结果
        
    Raises:
        HTTPException: 创建失败
    """
    try:
        index_name = ESIndex.get_index_name(knowledge_id)
        es_client.create_index(index_name, ESIndex.INDEX_BODY)
        return OperationResponse(
            success=True,
            message=f"Index {index_name} 创建成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"创建Index失败: {str(e)}"
        )


@router.delete("/{knowledge_id}", response_model=OperationResponse, summary="删除Index")
async def drop_index(knowledge_id: int):
    """
    删除Elasticsearch index
    
    Args:
        knowledge_id: 知识库ID
        
    Returns:
        操作结果
        
    Raises:
        HTTPException: 删除失败
    """
    try:
        index_name = ESIndex.get_index_name(knowledge_id)
        es_client.delete_index(index_name)
        return OperationResponse(
            success=True,
            message=f"Index {index_name} 删除成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除Index失败: {str(e)}"
        )
