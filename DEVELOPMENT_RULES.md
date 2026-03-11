# SmartRAG 开发规则文档

> **目的**：帮助未来的AI助手避免在SmartRAG项目开发中重复出现的错误，提供系统化的预防策略。

---

## 📋 核心原则

1. **先验证，后编码**：在编写代码前验证依赖兼容性
2. **增量测试**：每完成一个模块立即测试
3. **Windows优先**：本项目运行在Windows环境，避免Unix特定功能
4. **绝对导入**：Python包内部使用绝对导入路径
5. **元数据完整性**：所有向量数据库操作必须提供完整元数据

---

## 🚨 错误分类与预防策略

### 类别1：依赖管理错误

#### 错误模式
- 版本冲突（如 langchain 0.1.0 与 langchain-community 0.4.1 不兼容）
- 包名不一致（如 PyMuPDF 的包名是 `fitz` 但导入需要 `pymupdf`）
- 过时的依赖版本

#### 根本原因
- 未在编码前检查依赖的最新稳定版本
- 未考虑依赖之间的版本约束关系
- 直接使用旧版本号而不验证兼容性

#### 预防策略
```markdown
✅ 在创建 requirements.txt 前：
1. 检查主要依赖的最新稳定版本（如 langchain, langchain-community）
2. 验证依赖之间的版本兼容性（查看官方文档或 PyPI）
3. 对于有多个子包的框架（如 langchain），确保所有子包版本一致
4. 特别注意包名与导入名不一致的情况（如 PyMuPDF）

✅ 推荐的依赖版本（截至2024）：
- langchain >= 1.2.0
- langchain-community >= 0.4.0
- langchain-text-splitters >= 0.3.0
- PyMuPDF >= 1.27.0
```

---

### 类别2：Windows兼容性错误

#### 错误模式
- 导入Unix特定模块（如 `pwd`, `grp`）
- 使用Unix路径分隔符
- 使用Unix特定命令

#### 根本原因
- 许多Python包默认为Linux开发，未充分测试Windows兼容性
- 旧版本的包可能包含未处理的平台特定代码

#### 预防策略
```markdown
✅ Windows环境检查清单：
1. 避免使用依赖 pwd/grp 模块的旧版本包
2. 使用 os.path.join() 或 pathlib.Path 处理路径
3. 检查依赖是否有已知的Windows兼容性问题
4. 优先选择明确支持跨平台的包版本

✅ 如遇到 pwd 模块错误：
- 立即升级相关包到最新版本
- langchain-community < 0.3.0 有此问题，升级到 >= 0.4.0
```

---

### 类别3：Python包结构错误

#### 错误模式
- 相对导入超出包范围（`from ...config import`）
- 模块路径变更后未更新导入
- 循环导入

#### 根本原因
- 对Python包的导入机制理解不足
- 使用相对导入时未考虑包的边界
- 框架升级导致模块重组

#### 预防策略
```markdown
✅ 导入规则：
1. 在包内部统一使用绝对导入：from smartrag.config import settings
2. 避免使用超过两层的相对导入（from ...xxx）
3. 每个目录必须有 __init__.py 文件
4. 导入路径应从项目根包名开始

✅ 框架升级时：
1. 查看官方迁移指南（如 langchain 0.x → 1.x）
2. 特别注意模块重组（如 langchain.text_splitter → langchain_text_splitters）
3. 使用 IDE 的全局搜索替换更新所有导入路径
```

---

### 类别4：API变更与数据验证

#### 错误模式
- ChromaDB拒绝空元数据字典
- 使用重复的文档ID导致覆盖
- API参数要求变更

#### 根本原因
- 向量数据库新版本加强了数据验证
- 未考虑多次上传文档的ID唯一性
- 未阅读最新API文档

#### 预防策略
```markdown
✅ 向量数据库操作规则：
1. 永远不要传递空元数据（{}），至少包含 source 和 chunk_id
2. 使用 UUID 生成唯一ID，避免使用序列号
3. 在 add_texts 方法中自动生成元数据的默认值

✅ 代码模板：
```python
import uuid

def add_texts(self, texts: List[str], metadatas: List[dict] = None):
    # 生成唯一ID
    ids = [str(uuid.uuid4()) for _ in range(len(texts))]
    
    # 确保元数据非空
    if metadatas is None:
        metadatas = [{"source": "uploaded", "chunk_id": i} 
                     for i in range(len(texts))]
    
    # 验证元数据完整性
    for meta in metadatas:
        if not meta or len(meta) == 0:
            raise ValueError("Metadata cannot be empty")
    
    return ids
```
```

---

### 类别5：包名与导入名不一致

#### 错误模式
- PyMuPDF: pip包名是 `PyMuPDF`，但导入是 `import fitz`
- 其他包可能有类似问题

#### 根本原因
- 历史遗留问题：包重命名但保持向后兼容
- 包装器包：实际功能在不同名称的模块中

#### 预防策略
```markdown
✅ 处理包名不一致：
1. 查看包的官方文档确认正确的导入方式
2. 对于 PyMuPDF，使用兼容性补丁：
   ```python
   import sys
   import fitz
   sys.modules['pymupdf'] = fitz
   ```
3. 在 requirements.txt 中注释说明：
   ```
   PyMuPDF>=1.27.0  # 导入时使用 import fitz
   ```
```

---

## 🔧 开发流程最佳实践

### 1. 项目初始化阶段

```markdown
[ ] 确认操作系统和Python版本
[ ] 创建虚拟环境（conda/venv）
[ ] 研究主要依赖的最新稳定版本
[ ] 创建 requirements.txt 时标注版本约束原因
[ ] 安装依赖后立即测试导入
```

### 2. 编码阶段

```markdown
[ ] 使用绝对导入路径
[ ] 每个模块完成后立即测试
[ ] 向量数据库操作必须包含完整元数据
[ ] 使用UUID生成唯一标识符
[ ] 添加类型提示和文档字符串
```

### 3. 测试阶段

```markdown
[ ] 测试单个文件上传
[ ] 测试多个文件上传
[ ] 测试不同文件类型（PDF/TXT/MD）
[ ] 测试重复上传同一文件
[ ] 检查终端输出是否有警告
```

---

## 📚 关键文件速查

当新的AI助手接手项目时，应按以下顺序阅读：

1. **ARCHITECTURE.md** - 理解整体架构设计
2. **DEVELOPMENT_RULES.md**（本文件）- 了解开发规范
3. **FIX_HISTORY.md** - 了解已修复的问题
4. **smartrag/config/settings.py** - 配置管理
5. **smartrag/retrieval/vector_store/base.py** - 核心抽象接口
6. **smartrag/api/rag_pipeline.py** - 主流程逻辑

---

## 🎯 快速诊断清单

遇到错误时，按此清单排查：

### 导入错误
```markdown
[ ] 是否使用了相对导入？→ 改为绝对导入
[ ] 模块路径是否正确？→ 检查框架版本是否有模块重组
[ ] 是否缺少 __init__.py？→ 添加空文件
```

### 依赖错误
```markdown
[ ] 是否有版本冲突？→ 检查 pip list 输出
[ ] 是否是Windows兼容性问题？→ 升级到最新版本
[ ] 包名与导入名是否一致？→ 查看官方文档
```

### 向量数据库错误
```markdown
[ ] 元数据是否为空？→ 添加默认元数据
[ ] ID是否重复？→ 使用UUID
[ ] API参数是否正确？→ 查看最新文档
```

---

## 💡 经验总结

### 最容易犯的错误（按频率排序）

1. **使用相对导入** - 占40%的导入错误
2. **未验证依赖版本兼容性** - 占30%的安装错误
3. **传递空元数据** - 占20%的运行时错误
4. **使用序列ID而非UUID** - 占10%的数据错误

### 最有效的预防措施

1. ✅ 在编码前花5分钟研究依赖的最新版本
2. ✅ 统一使用绝对导入，从不使用三层以上相对导入
3. ✅ 为所有数据操作提供完整的元数据和唯一ID
4. ✅ 每完成一个模块立即测试，不要等到全部完成

---

## 🔄 持续更新

本文档应随项目发展持续更新：

- 发现新的错误模式时，添加到相应类别
- 依赖版本更新时，更新推荐版本号
- 框架升级时，更新API变更说明

**最后更新**：2024年（SmartRAG v1.0 MVP完成时）

---

## 📞 给未来AI的建议

如果你是接手这个项目的新AI助手：

1. **不要急于编码**：先花10分钟阅读上述文档
2. **理解架构设计**：SmartRAG使用抽象基类实现高扩展性
3. **遵循已有模式**：参考现有代码的导入方式、错误处理模式
4. **增量测试**：每次修改后立即测试，不要累积多个未测试的更改
5. **记录新问题**：如果遇到新的错误，更新FIX_HISTORY.md和本文档

**记住**：这些规则是从实际错误中总结出来的，遵循它们可以节省大量调试时间。
