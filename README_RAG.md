# Python RAG服务实现文档

## 概述

本项目实现了一个完整的RAG（Retrieval-Augmented Generation）知识库系统的Python服务部分，基于FastAPI和LangChain框架。

## 架构说明

### 技术栈

- **FastAPI**: Web框架
- **LangChain**: RAG统一抽象框架
- **PyPDFLoader & Docx2txtLoader**: 文档加载器
- **RecursiveCharacterTextSplitter**: 文本切片器
- **HuggingFaceEmbeddings**: 向量化封装（bge-small-zh-v1.5，512维）
- **Milvus**: 向量数据库
- **Elasticsearch**: 全文检索引擎（IK分词器）
- **MinIO**: 对象存储

### 服务职责

Python RAG服务负责：
1. 文档解析（PDF、Word）
2. 文本切片（200-1000字符，100字符重叠）
3. 向量化（512维向量）
4. 向量存储（Milvus）
5. 全文索引（Elasticsearch）
6. 混合检索（0.6向量 + 0.4全文）

## 项目结构

```
AgentProject/
├── agentproject/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── parse.py          # 文档解析API
│   │   │   ├── chunk.py          # 文档切片API
│   │   │   ├── embed.py          # 向量化API
│   │   │   ├── search.py         # 混合检索API
│   │   │   ├── collection.py     # Milvus Collection管理API
│   │   │   ├── index.py          # ES Index管理API
│   │   │   └── models.py         # Pydantic模型
│   │   └── router.py             # 路由注册
│   ├── services/
│   │   └── rag/
│   │       ├── document_loader.py    # 文档加载服务
│   │       ├── text_splitter.py      # 文本切片服务
│   │       ├── embeddings.py         # 向量化服务
│   │       ├── vector_store.py       # 向量存储服务
│   │       └── hybrid_retriever.py   # 混合检索服务
│   ├── utils/
│   │   ├── minio_client.py       # MinIO客户端
│   │   ├── es_client.py          # Elasticsearch客户端
│   │   └── milvus_client.py      # Milvus客户端
│   ├── config/
│   │   └── es_index.py           # ES索引配置
│   ├── config.yaml               # 配置文件
│   ├── settings.py               # 配置加载
│   └── main.py                   # 应用入口
├── requirements.txt              # Python依赖
└── README_RAG.md                 # 本文档
```

## 配置说明

### config.yaml配置项

```yaml
# 服务配置
server:
  host: "0.0.0.0"
  port: 7860
  project_name: "AgentProject RAG Service"
  version: "1.0.0"

# MySQL配置
mysql:
  host: "192.168.1.67"
  port: 3306
  user: "root"
  password: "123456"
  database: "ruoyi-vue-pro"

# Redis配置
redis:
  host: "192.168.1.67"
  port: 6379
  password: ""
  db: 1

# Elasticsearch配置
elasticsearch:
  url: "http://192.168.1.67:9201"
  api_key: "GB-EvnnR79X-ljvw6lYI"

# Milvus配置
milvus:
  host: "192.168.1.67"
  port: 19530
  user: "root"
  password: "Milvus"

# 向量化模型配置
embedding:
  service: "ollama"
  base_url: "http://192.168.1.70:11434"
  model: "bge-small-zh-v1.5"
  dimensions: 512

# MinIO配置
minio:
  endpoint: "192.168.1.67:9000"
  access_key: "minioadmin"
  secret_key: "minioadmin"
  bucket_name: "agentchat"
  secure: false
```

## API端点

### 1. 文档解析

**POST /api/v1/parse**

解析PDF或Word文档，提取文本内容。

请求体：
```json
{
  "document_uri": "path/to/document.pdf",
  "file_type": "pdf"
}
```

响应：
```json
{
  "content": "文档文本内容...",
  "char_count": 1234
}
```

### 2. 文档切片

**POST /api/v1/chunk**

将文本切片为多个片段。

请求体：
```json
{
  "content": "长文本内容...",
  "min_size": 200,
  "max_size": 1000,
  "overlap_size": 100
}
```

响应：
```json
{
  "chunks": [
    {
      "content": "切片内容1...",
      "sequence": 1,
      "char_count": 856
    }
  ]
}
```

### 3. 向量化和索引

**POST /api/v1/embed**

将切片向量化并存储到Milvus和Elasticsearch。

请求体：
```json
{
  "knowledge_id": 1,
  "slices": [
    {
      "slice_id": 1,
      "content": "切片内容...",
      "document_id": 1,
      "sequence": 1
    }
  ]
}
```

响应：
```json
{
  "success": true,
  "processed_count": 1
}
```

### 4. 混合检索

**POST /api/v1/search**

执行混合检索（向量检索 + 全文检索）。

请求体：
```json
{
  "knowledge_id": 1,
  "query": "查询问题",
  "top_k": 5
}
```

响应：
```json
{
  "results": [
    {
      "slice_id": 1,
      "document_id": 1,
      "content": "相关内容...",
      "vector_score": 0.85,
      "fulltext_score": 0.72,
      "final_score": 0.798,
      "rank": 1
    }
  ]
}
```

### 5. Collection管理

**POST /api/v1/collection/create?knowledge_id=1**

创建Milvus collection。

**DELETE /api/v1/collection/{knowledge_id}**

删除Milvus collection。

### 6. Index管理

**POST /api/v1/index/create?knowledge_id=1**

创建Elasticsearch index。

**DELETE /api/v1/index/{knowledge_id}**

删除Elasticsearch index。

## 安装和运行

### 1. 安装依赖

```bash
cd AgentProject
pip install -r requirements.txt
```

### 2. 配置文件

编辑 `agentproject/config.yaml`，配置各项服务连接信息。

### 3. 启动服务

```bash
python -m agentproject.main
```

或使用uvicorn：

```bash
uvicorn agentproject.main:app --host 0.0.0.0 --port 7860 --reload
```

### 4. 访问API文档

启动后访问：http://localhost:7860/docs

## 与Java后端集成

Java后端通过HTTP调用Python RAG服务的API端点。

### Java客户端示例

```java
@Component
public class PythonRagClient {
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Value("${python.rag.base-url}")
    private String baseUrl;  // http://localhost:7860/api/v1
    
    public ParseResponse parseDocument(String documentUri, String fileType) {
        ParseRequest request = new ParseRequest(documentUri, fileType);
        return restTemplate.postForObject(
            baseUrl + "/parse", 
            request, 
            ParseResponse.class
        );
    }
    
    public SearchResponse search(Long knowledgeId, String query) {
        SearchRequest request = new SearchRequest(knowledgeId, query, 5);
        return restTemplate.postForObject(
            baseUrl + "/search", 
            request, 
            SearchResponse.class
        );
    }
}
```

## 核心特性

### 1. LangChain集成

使用LangChain统一抽象简化RAG实现：

- **DocumentLoader**: PyPDFLoader和Docx2txtLoader加载文档
- **TextSplitter**: RecursiveCharacterTextSplitter智能切片
- **Embeddings**: HuggingFaceEmbeddings封装bge-small-zh-v1.5
- **VectorStore**: Milvus集成实现向量存储
- **Retriever**: EnsembleRetriever实现混合检索

### 2. 混合检索策略

- 向量检索权重：0.6
- 全文检索权重：0.4
- 最终分数阈值：0.3

### 3. 文本切片策略

- 切片大小：200-1000字符
- 重叠大小：100字符
- 分隔符优先级：段落 > 句子 > 标点 > 空格

### 4. 向量化

- 模型：bge-small-zh-v1.5
- 维度：512
- 归一化：启用

## 注意事项

1. **模型下载**: 首次运行时会自动下载bge-small-zh-v1.5模型（约400MB）
2. **内存要求**: 建议至少4GB可用内存
3. **Elasticsearch IK分词器**: 需要预先安装IK分词器插件
4. **Milvus版本**: 需要Milvus 2.3+
5. **并发处理**: 默认支持10个并发文档解析任务

## 故障排查

### 1. 模型加载失败

```bash
# 手动下载模型
huggingface-cli download BAAI/bge-small-zh-v1.5
```

### 2. Milvus连接失败

检查Milvus服务状态和连接配置。

### 3. Elasticsearch连接失败

检查ES服务状态、API Key和IK分词器安装。

### 4. MinIO连接失败

检查MinIO服务状态和访问密钥配置。

## 性能指标

- 文档解析：30秒内完成（50页PDF）
- 文本切片：即时完成
- 向量化：10秒内完成单个切片
- 混合检索：500毫秒内完成

## 后续优化

1. 添加批量处理优化
2. 实现缓存机制
3. 添加异步任务队列
4. 实现分布式部署
5. 添加监控和日志
