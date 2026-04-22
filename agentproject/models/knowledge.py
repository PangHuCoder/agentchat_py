"""
知识库模型
"""
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, SmallInteger
from sqlalchemy.orm import relationship
from .base import Base


class Knowledge(Base):
    """知识库表"""
    __tablename__ = 'knowledge'
    
    id = Column(BigInteger, primary_key=True, comment='主键ID')
    name = Column(String(255), nullable=False, comment='知识库名称')
    description = Column(String(1000), comment='知识库描述')
    icon_uri = Column(String(500), comment='图标URI')
    status = Column(SmallInteger, comment='状态 0=禁用,1=启用')
    doc_count = Column(Integer, comment='文档数量')
    slice_count = Column(BigInteger, comment='切片总数')
    create_time = Column(DateTime, comment='创建时间')
    creator = Column(String(64), comment='创建人')
    update_time = Column(DateTime, comment='更新时间')
    updater = Column(String(64), comment='更新人')
    
    # 关系
    documents = relationship("KnowledgeDocument", back_populates="knowledge")
    slices = relationship("KnowledgeDocumentSlice", back_populates="knowledge")
    conversations = relationship("Conversation", back_populates="knowledge")
