"""
文档解析API端点
"""
from fastapi import APIRouter, HTTPException
from agentproject.api.v1.models import ParseRequest, ParseResponse
from agentproject.services.rag.document_loader import DocumentLoaderService
from agentproject.utils.minio_client import minio_client
import os

router = APIRouter(prefix="/parse", tags=["文档解析"])

# 初始化服务
document_loader_service = DocumentLoaderService()


@router.post("", response_model=ParseResponse, summary="解析文档")
async def parse_document(request: ParseRequest):
    """
    解析文档，提取文本内容（使用LangChain DocumentLoader）
    
    Args:
        request: 解析请求，包含文档URI和文件类型
        
    Returns:
        解析后的文本内容和字符数
        
    Raises:
        HTTPException: 文档解析失败
    """
    temp_file_path = None
    try:
        # 1. 从MinIO下载文件到临时目录
        temp_file_path = await minio_client.download_file(request.document_uri)
        
        # 2. 根据file_type使用对应的LangChain Loader
        if request.file_type == "pdf":
            documents = document_loader_service.load_pdf(temp_file_path)
        elif request.file_type in ["docx", "doc"]:
            documents = document_loader_service.load_word(temp_file_path)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型: {request.file_type}"
            )
        
        # 3. 提取文本内容
        content = document_loader_service.extract_text(documents)
        
        return ParseResponse(
            content=content,
            char_count=len(content)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文档解析失败: {str(e)}"
        )
    finally:
        # 清理临时文件
        if temp_file_path:
            await minio_client.cleanup_temp_file(temp_file_path)
