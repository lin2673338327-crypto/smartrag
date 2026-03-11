import gradio as gr
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from smartrag.api.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()

def upload_files(files):
    if not files:
        return "❌ 请先选择文件", ""
    
    results = []
    total_chunks = 0
    
    for file in files:
        try:
            file_path = file.name
            file_name = Path(file_path).name
            chunks = pipeline.add_document(file_path)
            total_chunks += chunks
            results.append(f"✅ {file_name}: {chunks}个片段")
        except Exception as e:
            results.append(f"❌ {Path(file.name).name}: {str(e)}")
    
    status = "\n".join(results)
    file_list = "\n".join([f"📄 {f}" for f in pipeline.get_uploaded_files()])
    
    return f"处理完成！\n\n{status}\n\n总计: {total_chunks}个片段已存入向量库", file_list

def chat(message, history):
    if not pipeline.get_uploaded_files():
        return "⚠️ 请先上传文档"
    try:
        response = pipeline.query(message)
        return response
    except Exception as e:
        return f"❌ 查询失败: {str(e)}"

with gr.Blocks(title="SmartRAG") as demo:
    gr.Markdown("# 🤖 SmartRAG - 本地RAG系统")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📁 文档管理")
            file_input = gr.File(label="上传文档 (支持多选)", file_count="multiple", file_types=[".pdf", ".txt", ".md"])
            upload_btn = gr.Button("📤 上传", variant="primary")
            upload_output = gr.Textbox(label="上传状态", lines=5)
            
            gr.Markdown("### 📋 已上传文件")
            file_list = gr.Textbox(label="文件列表", lines=8, interactive=False)
        
        with gr.Column(scale=2):
            chatbot = gr.ChatInterface(
                fn=chat,
                title="💬 智能问答",
                examples=["这些文档的主要内容是什么？", "请总结关键信息", "文档中提到了哪些技术？"]
            )
    
    upload_btn.click(upload_files, inputs=file_input, outputs=[upload_output, file_list])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861)
