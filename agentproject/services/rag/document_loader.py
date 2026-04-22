"""
文档加载服务 - 使用 LangChain DocumentLoader
"""
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from typing import List
from langchain.schema import Document
from loguru import logger


class DocumentLoaderService:
    """文档加载服务 - 使用 LangChain 的 DocumentLoader"""
    
    def load_pdf(self, file_path: str) -> List[Document]:
        """
        加载 PDF 文档
        :param file_path: PDF 文件路径
        :return: Document 列表
        """
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            logger.info(f"Loaded PDF document: {file_path}, pages: {len(documents)}")
            return documents
        except Exception as e:
            logger.error(f"Failed to load PDF document: {e}")
            raise
    
    def load_word(self, file_path: str) -> List[Document]:
        """
        加载 Word 文档
        :param file_path: Word 文件路径
        :return: Document 列表
        """
        try:
            loader = Docx2txtLoader(file_path)
            documents = loader.load()
            logger.info(f"Loaded Word document: {file_path}")
            return documents
        except Exception as e:
            logger.error(f"Failed to load Word document: {e}")
            raise
    
    def extract_text(self, documents: List[Document]) -> str:
        """
        从 Document 列表中提取文本内容
        :param documents: Document 列表
        :return: 合并后的文本内容
        """
        try:
            # 合并所有页面的内容
            text = "\n\n".join([doc.page_content for doc in documents])
            logger.info(f"Extracted text, total chars: {len(text)}")
            return text
        except Exception as e:
            logger.error(f"Failed to extract text: {e}")
            raise


# 全局文档加载服务实例
document_loader_service = DocumentLoaderService()
