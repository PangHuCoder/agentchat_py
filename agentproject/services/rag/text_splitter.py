"""
文本切片服务 - 使用LangChain RecursiveCharacterTextSplitter
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List


class TextSplitterService:
    """使用LangChain的RecursiveCharacterTextSplitter切片文本"""
    
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
        )
    
    def split_text(self, text: str) -> List[str]:
        """
        切片文本，保持语义完整性
        
        Args:
            text: 待切片的文本内容
            
        Returns:
            切片列表，每个切片字符数在200-1000之间
        """
        chunks = self.splitter.split_text(text)
        # 过滤掉过短的切片
        return [chunk for chunk in chunks if len(chunk) >= 200]
