# SmartRAG - 本地RAG系统

基于Ollama + ChromaDB + LangChain的本地知识库问答系统

## 特性

- 🚀 **本地部署**: Ollama本地大模型，数据隐私安全
- 📚 **多格式支持**: PDF/TXT/Markdown文档解析
- 🔍 **语义检索**: 向量化存储，智能检索
- 🏗️ **扩展性设计**: 抽象基类，支持多向量库切换
- 💻 **简洁界面**: Gradio快速原型

## 快速开始

```bash
# 1. 激活环境
conda activate smartrag

# 2. 启动应用
python smartrag/ui/gradio_app.py

# 3. 访问界面
# http://localhost:7860
```

## 技术栈

- **大模型**: Ollama (qwen3:4b)
- **向量库**: ChromaDB + FAISS
- **框架**: LangChain
- **界面**: Gradio
- **文档解析**: PyMuPDF

## 项目结构

```
smartrag/
├── smartrag/           # 核心代码
│   ├── config/         # 配置模块
│   ├── document/       # 文档处理
│   ├── retrieval/      # 检索模块（含向量库抽象层）
│   ├── llm/            # 大模型模块
│   ├── api/            # 业务逻辑
│   └── ui/             # Gradio界面
├── data/               # 数据目录
├── ARCHITECTURE.md     # 架构设计文档
├── USAGE.md            # 使用指南
└── requirements.txt    # 依赖
```

## 架构亮点

1. **抽象基类设计**: `BaseVectorStore` 实现向量库扩展性
2. **分层架构**: UI → Pipeline → Module → Infrastructure
3. **配置化管理**: Pydantic Settings统一配置
4. **模块化设计**: 职责清晰，易于维护

详见 [ARCHITECTURE.md](ARCHITECTURE.md)

## 使用说明

详见 [USAGE.md](USAGE.md)

## 面试展示

本项目适合作为面试项目展示：
- ✅ 完整的RAG系统实现
- ✅ 良好的架构设计
- ✅ 扩展性考虑
- ✅ 工程化实践

---

**版本**: v0.1.0  
**技术栈**: Python 3.10 + Ollama + ChromaDB + LangChain
