"""
消息模型
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from .base import Base


class Message(Base):
    """消息表"""
    __tablename__ = 'message'
    
    id = Column(BigInteger, primary_key=True, comment='主键ID')
    conversation_id = Column(BigInteger, ForeignKey('conversation.id'), comment='所属对话ID')
    role = Column(String(20), comment='角色 user=用户,assistant=助手')
    content = Column(Text, comment='消息内容')
    create_time = Column(DateTime, comment='创建时间')
    
    # 关系
    conversation = relationship("Conversation", back_populates="messages")
    retrieval_records = relationship("MessageRetrievalRecord", back_populates="message")
