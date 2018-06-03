import sys
import requests
from config import OLLAMA_URL, OLLAMA_MODEL, TIMEOUT


def generate(prompt: str) -> str:
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()["response"]
    except requests.exceptions.ConnectionError:
        print("[ERROR] 请先运行 ollama serve")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"[ERROR] 请求超时（>{TIMEOUT}s），请检查模型是否已加载")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Ollama 请求失败: {e}")
        sys.exit(1)
