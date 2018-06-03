import os

OLLAMA_MODEL  = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
OLLAMA_URL    = os.getenv("OLLAMA_URL",   "http://localhost:11434/api/generate")
DATA_FILE     = "leetcode_problems.json"
SOLUTIONS_DIR = "solutions"
START_DATE    = "2018-06-04"
TIMEOUT       = int(os.getenv("OLLAMA_TIMEOUT", "300"))
