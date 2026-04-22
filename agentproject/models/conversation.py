"""
对话模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from .base import Base


class Conversation(Base):
    """对话表"""
    __tablename__ = 'conversation'
    
    id = Column(BigInteger, primary_key=True, comment='主键ID')
    name = Column(String(255), comment='对话名称')
    knowledge_id = Column(BigInteger, ForeignKey('knowledge.id'), comment='关联的知识库ID')
    user_id = Column(String(64), comment='用户ID')
    create_time = Column(DateTime, comment='创建时间')
    update_time = Column(DateTime, comment='更新时间')
    
    # 关系
    knowledge = relationship("Knowledge", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
