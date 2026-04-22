"""
文档切片API端点
"""
from fastapi import APIRouter, HTTPException
from agentproject.api.v1.models import ChunkRequest, ChunkResponse, ChunkItem
from agentproject.services.rag.text_splitter import TextSplitterService

router = APIRouter(prefix="/chunk", tags=["文档切片"])

# 初始化服务
text_splitter_service = TextSplitterService()


@router.post("", response_model=ChunkResponse, summary="切片文本")
async def chunk_text(request: ChunkRequest):
    """
    切片文本（使用LangChain RecursiveCharacterTextSplitter）
    
    Args:
        request: 切片请求，包含文本内容和切片参数
        
    Returns:
        切片列表
        
    Raises:
        HTTPException: 文本切片失败
    """
    try:
        # 使用LangChain的文本切片器
        chunks = text_splitter_service.split_text(request.content)
        
        # 构建响应
        chunk_items = [
            ChunkItem(
                content=chunk,
                sequence=i + 1,
                char_count=len(chunk)
            )
            for i, chunk in enumerate(chunks)
        ]
        
        return ChunkResponse(chunks=chunk_items)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文本切片失败: {str(e)}"
        )
