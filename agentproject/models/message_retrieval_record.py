"""
消息检索记录模型
"""
from sqlalchemy import Column, BigInteger, Integer, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from .base import Base


class MessageRetrievalRecord(Base):
    """消息检索记录表"""
    __tablename__ = 'message_retrieval_record'
    
    id = Column(BigInteger, primary_key=True, comment='主键ID')
    message_id = Column(BigInteger, ForeignKey('message.id'), comment='消息ID（assistant角色的回答消息）')
    slice_id = Column(BigInteger, ForeignKey('knowledge_document_slice.id'), comment='切片ID')
    vector_score = Column(DECIMAL(5, 4), comment='Milvus向量检索分数')
    fulltext_score = Column(DECIMAL(5, 4), comment='Elasticsearch全文检索分数')
    final_score = Column(DECIMAL(5, 4), comment='融合后的最终分数')
    ranking = Column(Integer, comment='最终排名（1表示最相关）')
    create_time = Column(DateTime, comment='创建时间')
    
    # 关系
    message = relationship("Message", back_populates="retrieval_records")
    slice = relationship("KnowledgeDocumentSlice", back_populates="retrieval_records")
