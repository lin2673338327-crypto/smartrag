# SmartRAG 使用指南

## 快速开始

### 1. 环境准备
```bash
# 激活环境
conda activate smartrag

# 确认Ollama运行
ollama list  # 应该看到qwen3:4b
```

### 2. 启动应用
```bash
# Windows
start.bat

# 或手动启动
python smartrag/ui/gradio_app.py
```

### 3. 使用流程
1. 打开浏览器访问 http://localhost:7860
2. 左侧上传文档（PDF/TXT/MD）
3. 点击"上传"按钮处理文档
4. 右侧聊天框输入问题
5. 系统基于文档内容回答

---

## 功能说明

### 文档处理
- 支持格式: PDF, TXT, Markdown
- 自动分块: 500字符/块，50字符重叠
- 向量化存储: ChromaDB持久化

### 智能问答
- 语义检索: Top-3相关片段
- 上下文增强: 自动注入检索结果
- 本地模型: qwen3:4b生成回答

---

## 配置说明

编辑 `.env` 文件（参考 `.env.example`）：

```bash
# 模型配置
OLLAMA_MODEL=qwen3:4b

# 分块配置
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# 向量库选择
VECTOR_STORE_TYPE=chromadb  # 或 faiss
```

---

## 常见问题

### Q1: 启动失败？
检查Ollama是否运行：
```bash
ollama serve
```

### Q2: 模型未找到？
下载模型：
```bash
ollama pull qwen3:4b
```

### Q3: 依赖安装失败？
使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 项目结构

```
smartrag/
├── smartrag/           # 核心代码
│   ├── config/         # 配置
│   ├── document/       # 文档处理
│   ├── retrieval/      # 检索模块
│   ├── llm/            # 大模型
│   ├── api/            # 业务逻辑
│   └── ui/             # 界面
├── data/               # 数据目录
├── scripts/            # 工具脚本
└── requirements.txt    # 依赖
```

---

## 扩展开发

### 添加新向量库
1. 继承 `BaseVectorStore`
2. 实现 `add_texts` 和 `similarity_search`
3. 在配置中切换

### 添加新文档格式
修改 [`processor.py`](smartrag/document/processor.py:1)，添加新的loader

### 切换LLM模型
修改配置文件中的 `OLLAMA_MODEL`

---

## 面试展示要点

1. **架构设计**: 分层架构 + 抽象基类
2. **扩展性**: 向量库工厂模式
3. **工程实践**: 配置管理 + 模块化
4. **技术深度**: RAG原理 + 向量检索

详见 [`ARCHITECTURE.md`](ARCHITECTURE.md:1)
