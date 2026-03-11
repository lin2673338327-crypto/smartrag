# SmartRAG 故障排查指南

## 常见问题解决

### 1. PyMuPDF导入错误
**错误**: `pymupdf package not found`

**原因**: PyMuPDF的Python包名是`fitz`，但pip安装名是`pymupdf`

**解决**: 
```bash
pip install pymupdf
# 验证
python -c "import fitz; print(fitz.__version__)"
```

### 2. 元数据错误
**错误**: `Expected metadata to be a non-empty dict, got {}`

**原因**: ChromaDB新版本要求元数据必须包含至少一个键值对

**解决**: 已在 [`chromadb.py`](smartrag/retrieval/vector_store/chromadb.py:13) 中修复，自动添加`source`和`chunk_id`

### 3. 端口占用
**错误**: `error while attempting to bind on address ('0.0.0.0', 7860)`

**原因**: 端口已被其他应用占用

**解决**: 
- 修改端口为7861
- 或关闭占用7860端口的应用

### 4. 相对导入错误
**错误**: `attempted relative import beyond top-level package`

**原因**: Python包导入路径问题

**解决**: 已修复，使用绝对导入`from smartrag.xxx import xxx`

### 5. langchain模块路径错误
**错误**: `No module named 'langchain.text_splitter'`

**原因**: langchain 1.x版本模块重构

**解决**: 使用`from langchain_text_splitters import RecursiveCharacterTextSplitter`

---

## 环境检查清单

运行前检查：
```bash
# 1. 检查conda环境
conda activate smartrag

# 2. 检查Ollama
python scripts/test_ollama.py

# 3. 检查依赖
pip list | findstr langchain
pip list | findstr chromadb
pip list | findstr pymupdf

# 4. 启动应用
python smartrag/ui/gradio_app.py
```

---

## 调试技巧

### 查看详细错误
修改 [`gradio_app.py`](smartrag/ui/gradio_app.py:11) 中的错误处理，已添加`traceback.format_exc()`显示完整堆栈

### 测试单个模块
```python
# 测试文档处理
from smartrag.document.processor import DocumentProcessor
processor = DocumentProcessor()
chunks = processor.load_and_split("test.pdf")
print(f"分块数: {len(chunks)}")

# 测试向量库
from smartrag.retrieval.vector_store.chromadb import ChromaDBStore
store = ChromaDBStore()
store.add_texts(["测试文本"])

# 测试Ollama
from smartrag.llm.ollama_client import OllamaClient
client = OllamaClient()
response = client.generate("你好")
print(response)
```

---

**更新时间**: 2026-03-10
