from fastapi import APIRouter
from agentchat.api.v1 import (chat, message, history,  knowledge)

router = APIRouter(prefix="/api/v1")

router.include_router(chat.router)
router.include_router(message.router)
router.include_router(history.router)
router.include_router(knowledge.router)
