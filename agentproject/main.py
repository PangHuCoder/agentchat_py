from fastapi import FastAPI
from contextlib import asynccontextmanager
from agentproject.api.router import router
from agentproject.settings import app_settings, initialize_app_settings
from agentproject.utils.minio_client import minio_client
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化配置
    logger.info("正在初始化应用配置...")
    await initialize_app_settings()
    logger.info("应用配置初始化完成")
    
    # 初始化MinIO客户端
    logger.info("正在初始化MinIO客户端...")
    minio_client.initialize()
    logger.info("MinIO客户端初始化完成")
    
    yield
    
    # 关闭时清理资源
    logger.info("应用正在关闭...")


app = FastAPI(
    title=app_settings.server.get("project_name", "AgentProject"),
    version=app_settings.server.get("version", "1.0.0"),
    lifespan=lifespan
)

# 注册路由
app.include_router(router)


@app.get("/", summary="健康检查")
async def health_check():
    """健康检查端点"""
    return {
        "status": "ok",
        "project": app_settings.server.get("project_name", "AgentProject"),
        "version": app_settings.server.get("version", "1.0.0")
    }


if __name__ == "__main__":
    import uvicorn
    
    host = app_settings.server.get("host", "0.0.0.0")
    port = app_settings.server.get("port", 7860)
    
    uvicorn.run(
        "agentproject.main:app",
        host=host,
        port=port,
        reload=True
    )