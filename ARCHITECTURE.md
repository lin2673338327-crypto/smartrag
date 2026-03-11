# SmartRAG 完整架构设计文档

## 1. MVP核心功能定义

### 1.1 核心功能
- 文档上传与解析（PDF/TXT/MD）
- 文本分块与向量化
- 双向量库支持（ChromaDB + FAISS）
- 语义检索
- Ollama本地大模型问答
- Gradio Web界面

### 1.2 核心流程
```
文档上传 → 解析分块 → 向量化 → 存储 → 用户提问 → 检索 → LLM生成
```

---

## 2. 架构设计

### 2.1 分层架构
```
┌─────────────────────────────────────┐
│   Presentation Layer (Gradio UI)    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Business Logic (RAGPipeline)      │
└─────────────────────────────────────┘
              ↓
┌──────────────┬──────────────────────┐
│ Document     │ Retrieval │ LLM      │
│ Processor    │ Module    │ Client   │
└──────────────┴──────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ ChromaDB │ FAISS │ Ollama Server    │
└─────────────────────────────────────┘
```

### 2.2 核心模块

#### Document Module
- [`DocumentProcessor`](smartrag/document/processor.py:1): 文档加载与分块
- 支持格式: PDF, TXT, Markdown
- 分块策略: RecursiveCharacterTextSplitter

#### Retrieval Module
- [`BaseVectorStore`](smartrag/retrieval/vector_store/base.py:1): 向量库抽象基类（扩展性关键）
- [`ChromaDBStore`](smartrag/retrieval/vector_store/chromadb.py:1): 持久化存储
- [`FAISSStore`](smartrag/retrieval/vector_store/faiss.py:1): 内存高性能检索（待实现）

#### LLM Module
- [`OllamaClient`](smartrag/llm/ollama_client.py:1): Ollama API封装
- [`PromptTemplate`](smartrag/llm/prompt.py:1): RAG提示词模板

---

## 3. 技术栈选型

| 组件 | 技术 | 理由 |
|------|------|------|
| 大模型 | Ollama (qwen3:4b) | 本地部署、免费 |
| 向量库 | ChromaDB + FAISS | 持久化 + 高性能 |
| 框架 | LangChain | RAG标准框架 |
| Embedding | bge-small-zh-v1.5 | 中文优化 |
| Web | Gradio | 快速原型 |
| 文档解析 | PyMuPDF | 高效PDF解析 |

---

## 4. 目录结构

```
smartrag/
├── smartrag/
│   ├── config/              # 配置模块
│   │   ├── settings.py      # Pydantic配置
│   ├── document/            # 文档处理
│   │   └── processor.py     # 文档加载分块
│   ├── retrieval/           # 检索模块
│   │   └── vector_store/    # 向量库
│   │       ├── base.py      # 抽象基类
│   │       ├── chromadb.py  # ChromaDB实现
│   │       └── faiss.py     # FAISS实现
│   ├── llm/                 # 大模型模块
│   │   ├── ollama_client.py # Ollama客户端
│   │   └── prompt.py        # 提示词模板
│   ├── api/                 # 业务逻辑
│   │   └── rag_pipeline.py  # RAG主流程
│   └── ui/                  # 界面
│       └── gradio_app.py    # Gradio应用
├── data/                    # 数据目录
│   ├── uploads/             # 上传文档
│   └── vector_db/           # 向量库
├── scripts/                 # 工具脚本
│   └── test_ollama.py       # Ollama测试
├── requirements.txt         # 依赖
└── start.bat               # 启动脚本
```

---

## 5. 实施路线图

### Phase 1: 基础框架 ✅
- [x] 项目结构创建
- [x] 配置模块
- [x] 依赖管理

### Phase 2: 核心模块 ✅
- [x] 文档处理器
- [x] ChromaDB向量库
- [x] Ollama客户端
- [x] RAG Pipeline

### Phase 3: 界面与测试 ✅
- [x] Gradio界面
- [x] Ollama连接测试
- [x] 启动脚本

### Phase 4: 扩展功能（可选）
- [ ] FAISS向量库完整实现
- [ ] FastAPI RESTful API
- [ ] 流式输出
- [ ] 重排序模块

---

## 6. 面试亮点

### 6.1 架构设计
1. **抽象基类设计**: [`BaseVectorStore`](smartrag/retrieval/vector_store/base.py:1) 实现向量库扩展性
2. **分层架构**: UI → Pipeline → Module → Infrastructure
3. **配置管理**: Pydantic Settings统一配置

### 6.2 扩展性
1. **向量库切换**: 通过基类抽象，新增向量库只需实现接口
2. **文档格式扩展**: 策略模式支持新格式
3. **模型切换**: 配置化模型选择

### 6.3 工程实践
1. **依赖管理**: requirements.txt + conda环境
2. **代码组织**: 模块化设计，职责清晰
3. **错误处理**: 异常捕获与用户友好提示

### 6.4 技术深度展示
**问题1: 为什么选择双向量库？**
> ChromaDB提供持久化，适合生产；FAISS提供极致性能，适合实时检索。通过抽象基类设计，可根据场景灵活切换。

**问题2: 如何保证扩展性？**
> 1. [`BaseVectorStore`](smartrag/retrieval/vector_store/base.py:1) 抽象基类定义统一接口
> 2. 新增向量库只需继承基类实现3个方法
> 3. 配置化切换，无需修改业务代码

**问题3: RAG核心原理？**
> 1. 文档分块避免上下文窗口限制
> 2. 向量化实现语义检索
> 3. Top-K检索获取相关片段
> 4. 上下文注入提示词增强LLM回答准确性

---

## 7. 快速启动

### 环境准备
```bash
# 1. 创建conda环境
conda create -n smartrag python=3.10 -y
conda activate smartrag

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动Ollama（如未启动）
ollama serve

# 4. 确保模型已下载
ollama pull qwen3:4b
```

### 运行应用
```bash
# Windows
start.bat

# 或直接运行
python smartrag/ui/gradio_app.py
```

访问: http://localhost:7860

---

## 8. 关键代码说明

### 8.1 向量库抽象层
[`base.py`](smartrag/retrieval/vector_store/base.py:1) 定义统一接口，实现多向量库支持

### 8.2 RAG Pipeline
[`rag_pipeline.py`](smartrag/api/rag_pipeline.py:1) 封装完整RAG流程：
1. 文档处理
2. 向量存储
3. 检索增强
4. LLM生成

### 8.3 Ollama集成
[`ollama_client.py`](smartrag/llm/ollama_client.py:1) 封装HTTP API调用，支持流式输出

---

**版本**: v1.0  
**创建时间**: 2026-03-09  
**技术栈**: Ollama + ChromaDB + FAISS + LangChain + Gradio
