"""
SQLAlchemy基础配置
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from agentproject.settings import app_settings

# 创建数据库引擎
def get_database_url():
    """获取数据库连接URL"""
    mysql_config = app_settings.mysql
    return f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['database']}?charset=utf8mb4"

engine = create_engine(
    get_database_url(),
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# 创建Session工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 依赖注入：获取数据库会话
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
