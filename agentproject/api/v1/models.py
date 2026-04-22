"""
API请求和响应模型
"""
from pydantic import BaseModel, Field
from typing import List, Optional


# ========== 文档解析相关 ==========

class ParseRequest(BaseModel):
    """文档解析请求"""
    document_uri: str = Field(..., description="文档URI")
    file_type: str = Field(..., description="文件类型：pdf, docx, doc")


class ParseResponse(BaseModel):
    """文档解析响应"""
    content: str = Field(..., description="解析后的文本内容")
    char_count: int = Field(..., description="字符数")


# ========== 文档切片相关 ==========

class ChunkRequest(BaseModel):
    """文档切片请求"""
    content: str = Field(..., description="待切片的文本内容")
    min_size: int = Field(default=200, description="最小切片大小")
    max_size: int = Field(default=1000, description="最大切片大小")
    overlap_size: int = Field(default=100, description="重叠大小")


class ChunkItem(BaseModel):
    """切片项"""
    content: str = Field(..., description="切片内容")
    sequence: int = Field(..., description="切片序号")
    char_count: int = Field(..., description="字符数")


class ChunkResponse(BaseModel):
    """文档切片响应"""
    chunks: List[ChunkItem] = Field(..., description="切片列表")


# ========== 向量化相关 ==========

class SliceData(BaseModel):
    """切片数据"""
    slice_id: int = Field(..., description="切片ID")
    content: str = Field(..., description="切片内容")
    document_id: Optional[int] = Field(None, description="文档ID")
    sequence: Optional[int] = Field(None, description="切片序号")


class EmbedRequest(BaseModel):
    """向量化请求"""
    knowledge_id: int = Field(..., description="知识库ID")
    slices: List[SliceData] = Field(..., description="切片数据列表")


class EmbedResponse(BaseModel):
    """向量化响应"""
    success: bool = Field(..., description="是否成功")
    processed_count: int = Field(..., description="处理数量")


# ========== 混合检索相关 ==========

class SearchRequest(BaseModel):
    """混合检索请求"""
    knowledge_id: int = Field(..., description="知识库ID")
    query: str = Field(..., description="查询文本")
    top_k: int = Field(default=5, description="返回结果数量")


class SearchResultItem(BaseModel):
    """检索结果项"""
    slice_id: int = Field(..., description="切片ID")
    document_id: Optional[int] = Field(None, description="文档ID")
    content: Optional[str] = Field(None, description="切片内容")
    vector_score: float = Field(..., description="向量检索分数")
    fulltext_score: float = Field(..., description="全文检索分数")
    final_score: float = Field(..., description="最终分数")
    rank: int = Field(..., description="排名")


class SearchResponse(BaseModel):
    """混合检索响应"""
    results: List[SearchResultItem] = Field(..., description="检索结果列表")


# ========== Collection和Index管理相关 ==========

class CollectionRequest(BaseModel):
    """Collection创建请求"""
    knowledge_id: int = Field(..., description="知识库ID")


class IndexRequest(BaseModel):
    """Index创建请求"""
    knowledge_id: int = Field(..., description="知识库ID")


class OperationResponse(BaseModel):
    """操作响应"""
    success: bool = Field(..., description="是否成功")
    message: Optional[str] = Field(None, description="消息")
