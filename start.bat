@echo off
echo 启动SmartRAG系统...
echo.

cd /d %~dp0..
call conda activate smartrag

echo 检查Ollama连接...
python scripts/test_ollama.py
if errorlevel 1 (
    echo.
    echo ❌ Ollama未启动或qwen3:4b模型未加载
    echo 请先启动Ollama: ollama serve
    echo 并加载模型: ollama pull qwen3:4b
    pause
    exit /b 1
)

echo.
echo 启动Gradio界面...
python smartrag/ui/gradio_app.py
