# SmartRAG 问题修复记录

## 修复时间线
**日期**: 2026-03-10  
**版本**: v1.0 → v1.1

---

## 修复问题清单

### 1. Windows系统pwd模块兼容性问题 ✅
**问题描述**: 
```
ModuleNotFoundError: No module named 'pwd'
```

**原因**: `pwd`是Unix/Linux系统模块，Windows不支持。langchain-community 0.0.20版本的pebblo模块依赖此模块。

**解决方案**:
```bash
pip uninstall langchain-community -y
pip install langchain-community --upgrade  # 升级到0.4.1
```

**修改文件**: 无需修改代码，仅升级依赖

---

### 2. Langchain版本兼容性问题 ✅
**问题描述**:
```
langchain 0.1.0 requires langchain-community<0.1, but you have langchain-community 0.4.1
```

**原因**: langchain 0.1.0与新版langchain-community不兼容

**解决方案**:
```bash
pip install langchain --upgrade  # 升级到1.2.10
```

**影响**: 模块导入路径变更

---

### 3. Langchain模块路径变更 ✅
**问题描述**:
```
ModuleNotFoundError: No module named 'langchain.text_splitter'
```

**原因**: langchain 1.x版本将text_splitter独立为langchain_text_splitters包

**解决方案**:
修改 [`processor.py`](smartrag/smartrag/document/processor.py:2)
```python
# 旧版
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 新版
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

---

### 4. 相对导入路径错误 ✅
**问题描述**:
```
ImportError: attempted relative import beyond top-level package
```

**原因**: Python包结构中相对导入层级超出顶层包

**解决方案**:
将所有相对导入改为绝对导入

**修改文件**:
- [`chromadb.py`](smartrag/smartrag/retrieval/vector_store/chromadb.py:3): `from ...config` → `from smartrag.config`
- [`processor.py`](smartrag/smartrag/document/processor.py:5): `from ..config` → `from smartrag.config`
- [`ollama_client.py`](smartrag/smartrag/llm/ollama_client.py:3): `from ...config` → `from smartrag.config`
- [`rag_pipeline.py`](smartrag/smartrag/api/rag_pipeline.py:1): `from ..xxx` → `from smartrag.xxx`

---

### 5. ChromaDB元数据验证错误 ✅
**问题描述**:
```
Expected metadata to be a non-empty dict, got {}
```

**原因**: ChromaDB新版本要求元数据必须包含至少一个键值对，空字典`{}`不被接受

**解决方案**:
修改 [`chromadb.py`](smartrag/smartrag/retrieval/vector_store/chromadb.py:13)
```python
# 旧版
metadatas = [{}] * len(texts)

# 新版
metadatas = [{"source": file_name, "chunk_id": i} for i in range(len(texts))]
```

---

### 6. PyMuPDF导入问题 ✅
**问题描述**:
```
ModuleNotFoundError: No module named 'pymupdf'
ImportError: pymupdf package not found
```

**原因**: PyMuPDF的Python包名是`fitz`，但langchain_community期望`import pymupdf`

**解决方案**:
1. 升级PyMuPDF到最新版本
```bash
pip install PyMuPDF --upgrade  # 1.23.0 → 1.27.1
```

2. 添加模块别名映射 [`processor.py`](smartrag/smartrag/document/processor.py:6)
```python
import sys
import fitz
sys.modules['pymupdf'] = fitz
```

---

### 7. ChromaDB ID冲突问题 ✅
**问题描述**:
```
Insert of existing embedding ID: doc_0
Add of existing embedding ID: doc_0
```

**原因**: 使用固定ID模式`doc_0, doc_1...`导致多次上传时ID重复，文档被覆盖

**解决方案**:
修改 [`chromadb.py`](smartrag/smartrag/retrieval/vector_store/chromadb.py:12)
```python
# 旧版
ids = [f"doc_{i}" for i in range(len(texts))]

# 新版
import uuid
ids = [str(uuid.uuid4()) for _ in range(len(texts))]
```

---

### 8. 端口占用问题 ✅
**问题描述**:
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 7860)
```

**原因**: 端口7860已被其他应用占用

**解决方案**:
修改 [`gradio_app.py`](smartrag/smartrag/ui/gradio_app.py:36)
```python
demo.launch(server_name="0.0.0.0", server_port=7861)
```

---

## 功能增强

### 9. 多文件上传支持 ✅
**需求**: 支持同时上传多个文档

**实现**: 修改 [`gradio_app.py`](smartrag/smartrag/ui/gradio_app.py:23)
```python
file_input = gr.File(
    label="上传文档 (支持多选)", 
    file_count="multiple",
    file_types=[".pdf", ".txt", ".md"]
)
```

**新增功能**:
- 批量上传PDF/TXT/MD文件
- 显示每个文件的处理结果
- 统计总分块数

---

### 10. 文件列表显示 ✅
**需求**: 查看已上传的文件列表

**实现**: 
1. [`rag_pipeline.py`](smartrag/smartrag/api/rag_pipeline.py:23) 添加文件追踪
```python
self.uploaded_files = []

def get_uploaded_files(self):
    return self.uploaded_files
```

2. [`gradio_app.py`](smartrag/smartrag/ui/gradio_app.py:28) 添加文件列表组件
```python
file_list = gr.Textbox(label="文件列表", lines=8)
```

---

### 11. 上传反馈优化 ✅
**改进**: 更清晰的成功/失败提示

**实现**: [`gradio_app.py`](smartrag/smartrag/ui/gradio_app.py:11)
```python
# 成功
✅ {file_name}: {chunks}个片段

# 失败
❌ {file_name}: {error_message}

# 详细错误
import traceback
error_detail = traceback.format_exc()
```

---

## 依赖版本变更

| 包名 | 旧版本 | 新版本 | 原因 |
|------|--------|--------|------|
| langchain | 0.1.0 | 1.2.10 | 兼容性 |
| langchain-community | 0.0.20 | 0.4.1 | Windows兼容 |
| langchain-core | 0.1.23 | 1.2.18 | 依赖升级 |
| PyMuPDF | 1.23.0 | 1.27.1 | 导入问题 |
| requests | 2.31.0 | 2.32.5 | 依赖升级 |
| pydantic-settings | 2.1.0 | 2.13.1 | 依赖升级 |

---

## 测试验证

### 测试用例
1. ✅ PDF文档上传
2. ✅ TXT文档上传
3. ✅ MD文档上传
4. ✅ 多文件批量上传
5. ✅ 混合格式上传（PDF+TXT+MD）
6. ✅ 文件列表显示
7. ✅ 智能问答功能

### 测试环境
- 操作系统: Windows 10
- Python: 3.10
- Conda环境: smartrag
- Ollama模型: qwen3:4b

---

## 已知问题

### 非关键警告
1. ChromaDB遥测警告（可忽略）
```
Failed to send telemetry event: capture() takes 1 positional argument but 3 were given
```

2. Gradio版本提示（可选升级）
```
IMPORTANT: You are using gradio version 4.16.0, however version 4.44.1 is available
```

---

## 文件修改汇总

| 文件 | 修改类型 | 说明 |
|------|---------|------|
| [`processor.py`](smartrag/smartrag/document/processor.py:1) | 修复+增强 | 模块导入+PyMuPDF兼容 |
| [`chromadb.py`](smartrag/smartrag/retrieval/vector_store/chromadb.py:1) | 修复 | 元数据+UUID |
| [`rag_pipeline.py`](smartrag/smartrag/api/rag_pipeline.py:1) | 增强 | 文件追踪 |
| [`gradio_app.py`](smartrag/smartrag/ui/gradio_app.py:1) | 增强 | 多文件+列表 |
| [`ollama_client.py`](smartrag/smartrag/llm/ollama_client.py:1) | 修复 | 导入路径 |
| [`requirements.txt`](smartrag/requirements.txt:1) | 更新 | 版本升级 |

---

**文档版本**: v1.1  
**最后更新**: 2026-03-10
