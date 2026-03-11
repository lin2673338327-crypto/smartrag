import requests
import sys

def test_ollama():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print("[OK] Ollama connection successful")
            print(f"Available models: {[m['name'] for m in models]}")
            
            if any("qwen3" in m['name'] for m in models):
                print("[OK] qwen3:4b model ready")
                return True
            else:
                print("[ERROR] qwen3:4b model not found")
                print("Run: ollama pull qwen3:4b")
                return False
        else:
            print("[ERROR] Ollama connection failed")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        print("Please start Ollama: ollama serve")
        return False

if __name__ == "__main__":
    if test_ollama():
        sys.exit(0)
    else:
        sys.exit(1)
