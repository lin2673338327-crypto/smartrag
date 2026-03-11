# SmartRAG

🚀 一个本地部署的RAG（检索增强生成）系统，支持Ollama本地大模型和ChromaDB/FAISS双向量数据库。

## ✨ 特性

- 🏠 **完全本地化部署** - 支持Ollama本地大模型，数据隐私有保障
- 🔄 **双向量数据库** - ChromaDB（持久化存储）+ FAISS（高性能检索）
- 📄 **多格式支持** - 支持PDF、TXT、MD文档上传和解析
- ⚡ **高性能** - 平均响应时间9.9ms
- 🎨 **友好界面** - 基于Gradio的Web界面，简单易用
- 🔧 **高扩展性** - 抽象基类设计，易于扩展其他向量数据库

## 🛠️ 技术栈

- **LLM**: Ollama (Qwen3:4b)
- **向量数据库**: ChromaDB, FAISS
- **Embedding**: BAAI/bge-small-zh-v1.5
- **框架**: LangChain, Gradio
- **语言**: Python 3.11+

## 📦 安装

### 前置要求

1. 安装 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. 安装 [Ollama](https://ollama.ai/)
3. 下载模型：`ollama pull qwen3:4b`

### 快速开始

```bash
# 克隆仓库
git clone https://github.com/lin2673338327-crypto/smartrag.git
cd smartrag

# 创建虚拟环境
conda create -n smartrag python=3.11 -y
conda activate smartrag

# 安装依赖
pip install -r requirements.txt

# 启动应用
python smartrag/ui/gradio_app.py
```

访问 http://localhost:7861 开始使用。

## 🚀 使用方法

1. **上传文档** - 支持批量上传PDF/TXT/MD文件
2. **查看文件列表** - 实时显示已上传的文档
3. **智能问答** - 基于上传的文档进行问答
4. **切换向量库** - 在ChromaDB和FAISS之间切换

## 📊 性能指标

- **响应速度**: 平均9.9ms (P95: 11ms)
- **语义理解**: 同义词识别准确率67%-100%
- **排序质量**: 相似度区分度0.344（优秀）

## 🏗️ 架构设计

```
smartrag/
├── config/          # 配置管理
├── retrieval/       # 检索模块
│   └── vector_store/  # 向量数据库（抽象基类设计）
├── document/        # 文档处理
├── llm/            # LLM集成
├── api/            # RAG Pipeline
└── ui/             # Gradio界面
```

## 🔧 配置

编辑 `.env` 文件自定义配置：

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:4b
EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5
VECTOR_STORE_TYPE=chromadb
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

## 📝 开发

```bash
# 运行评估测试
python test_evaluation.py

# 测试Ollama连接
python scripts/test_ollama.py
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 👤 作者

林鑫韬 - AI应用开发

---

⭐ 如果这个项目对你有帮助，欢迎Star！
