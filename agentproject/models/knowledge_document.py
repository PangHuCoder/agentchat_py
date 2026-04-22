"""
知识库文档模型
"""
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from .base import Base


class KnowledgeDocument(Base):
    """知识库文档表"""
    __tablename__ = 'knowledge_document'
    
    id = Column(BigInteger, primary_key=True, comment='主键ID')
    knowledge_id = Column(BigInteger, ForeignKey('knowledge.id'), comment='所属知识库ID')
    name = Column(String(500), comment='文档名称')
    file_extension = Column(String(20), comment='文件扩展名')
    uri = Column(String(1000), comment='文件URI')
    size = Column(BigInteger, comment='文件大小（字节）')
    slice_count = Column(Integer, comment='切片数量')
    char_count = Column(BigInteger, comment='字符数量')
    status = Column(SmallInteger, comment='状态 0=处理中,1=已完成,2=失败')
    fail_reason = Column(String(500), comment='失败原因')
    create_time = Column(DateTime, comment='创建时间')
    creator = Column(String(64), comment='创建人')
    update_time = Column(DateTime, comment='更新时间')
    updater = Column(String(64), comment='更新人')
    
    # 关系
    knowledge = relationship("Knowledge", back_populates="documents")
    slices = relationship("KnowledgeDocumentSlice", back_populates="document")
