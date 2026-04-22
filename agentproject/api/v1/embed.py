"""
向量化和索引API端点
"""
from fastapi import APIRouter, HTTPException
from agentproject.api.v1.models import EmbedRequest, EmbedResponse
from agentproject.services.rag.embeddings import EmbeddingService
from agentproject.services.rag.vector_store import VectorStoreService
from agentproject.utils.es_client import ESClient
from agentproject.settings import app_settings

router = APIRouter(prefix="/embed", tags=["向量化"])

# 初始化服务
embedding_service = EmbeddingService()
milvus_uri = f"http://{app_settings.milvus.get('host', 'localhost')}:{app_settings.milvus.get('port', 19530)}"
vector_store_service = VectorStoreService(milvus_uri, embedding_service)
es_client = ESClient()


@router.post("", response_model=EmbedResponse, summary="向量化切片并索引")
async def embed_slices(request: EmbedRequest):
    """
    向量化切片并索引（使用LangChain Milvus VectorStore）
    
    Args:
        request: 向量化请求，包含知识库ID和切片数据列表
        
    Returns:
        处理结果
        
    Raises:
        HTTPException: 向量化或索引失败
    """
    try:
        # 1. 获取或创建VectorStore
        vector_store = vector_store_service.create_collection(request.knowledge_id)
        
        # 2. 准备数据
        texts = [slice_data.content for slice_data in request.slices]
        ids = [str(slice_data.slice_id) for slice_data in request.slices]
        metadatas = [
            {
                "slice_id": slice_data.slice_id,
                "document_id": slice_data.document_id,
                "knowledge_id": request.knowledge_id
            }
            for slice_data in request.slices
        ]
        
        # 3. 使用LangChain VectorStore添加文档（自动向量化并存储到Milvus）
        vector_store_service.add_documents(
            vector_store=vector_store,
            texts=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        # 4. 同时索引到Elasticsearch
        index_name = f"knowledge_slice_{request.knowledge_id}"
        for slice_data in request.slices:
            es_client.index_document(
                index_name=index_name,
                doc_id=slice_data.slice_id,
                document={
                    "slice_id": slice_data.slice_id,
                    "document_id": slice_data.document_id,
                    "knowledge_id": request.knowledge_id,
                    "content": slice_data.content,
                    "sequence": slice_data.sequence or 0
                }
            )
        
        return EmbedResponse(
            success=True,
            processed_count=len(request.slices)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"向量化或索引失败: {str(e)}"
        )
