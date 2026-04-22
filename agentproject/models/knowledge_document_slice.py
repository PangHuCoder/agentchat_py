"""
知识库文档切片模型
"""
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, SmallInteger, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from .base import Base


class KnowledgeDocumentSlice(Base):
    """知识库文档切片表"""
    __tablename__ = 'knowledge_document_slice'
    
    id = Column(BigInteger, primary_key=True, comment='主键ID')
    knowledge_id = Column(BigInteger, ForeignKey('knowledge.id'), comment='所属知识库ID')
    document_id = Column(BigInteger, ForeignKey('knowledge_document.id'), comment='所属文档ID')
    document_name = Column(String(100), comment='文档名称')
    content = Column(Text, comment='切片内容')
    sequence = Column(Float, comment='切片序号')
    status = Column(SmallInteger, comment='状态 0=处理中,1=完成,2=失败')
    fail_reason = Column(String(500), comment='失败原因')
    char_count = Column(Integer, comment='字符数')
    create_time = Column(DateTime, comment='创建时间')
    creator = Column(String(64), comment='创建人')
    update_time = Column(DateTime, comment='更新时间')
    updater = Column(String(64), comment='更新人')
    
    # 关系
    knowledge = relationship("Knowledge", back_populates="slices")
    document = relationship("KnowledgeDocument", back_populates="slices")
    retrieval_records = relationship("MessageRetrievalRecord", back_populates="slice")
