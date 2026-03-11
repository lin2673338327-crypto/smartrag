from typing import List

class PromptTemplate:
    @staticmethod
    def build_rag_prompt(query: str, contexts: List[str]) -> str:
        context_str = "\n\n".join([f"[文档{i+1}]\n{ctx}" for i, ctx in enumerate(contexts)])
        return f"""你是一个智能助手，请基于以下文档内容回答用户问题。

文档内容：
{context_str}

用户问题：{query}

请根据文档内容给出准确、简洁的回答。如果文档中没有相关信息，请明确说明。"""
