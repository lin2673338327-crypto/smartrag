# SmartRAG 快速启动指南

## 一键启动

```bash
# Windows
start.bat
```

## 手动启动

### 1. 激活环境
```bash
conda activate smartrag
```

### 2. 检查Ollama
```bash
python scripts/test_ollama.py
```

### 3. 启动应用
```bash
python smartrag/ui/gradio_app.py
```

### 4. 访问界面
http://localhost:7860

---

## 使用示例

### 上传文档
1. 点击"上传文档"选择文件
2. 点击"上传"按钮
3. 等待处理完成

### 智能问答
在聊天框输入问题，例如：
- "这篇文档的主要内容是什么？"
- "请总结关键信息"
- "文档中提到了哪些技术？"

---

## 故障排查

### Ollama未启动
```bash
ollama serve
```

### 模型未下载
```bash
ollama pull qwen3:4b
```

### 依赖未安装
```bash
pip install -r requirements.txt
```

---

## 配置调整

编辑 `.env` 文件：
```bash
# 模型配置
OLLAMA_MODEL=qwen3:4b

# 分块大小（影响检索精度）
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# 向量库选择
VECTOR_STORE_TYPE=chromadb
```

---

## 项目文档

- [`README.md`](README.md:1) - 项目概述
- [`ARCHITECTURE.md`](ARCHITECTURE.md:1) - 架构设计
- [`USAGE.md`](USAGE.md:1) - 详细使用说明
- [`INTERVIEW_GUIDE.md`](INTERVIEW_GUIDE.md:1) - 面试展示指南
