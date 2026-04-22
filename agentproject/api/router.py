from fastapi import APIRouter
from agentproject.api.v1 import (
    chat, message, history, knowledge,
    parse, chunk, embed, search, collection, index
)

router = APIRouter(prefix="/api/v1")

# 原有路由
router.include_router(chat.router)
router.include_router(message.router)
router.include_router(history.router)
router.include_router(knowledge.router)

# RAG服务路由
router.include_router(parse.router)
router.include_router(chunk.router)
router.include_router(embed.router)
router.include_router(search.router)
router.include_router(collection.router)
router.include_router(index.router)
