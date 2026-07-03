# Daily LeetCode

Generates bilingual (EN + ZH) LeetCode solution notes and commits them with historical dates from **2018-06-04** to **2026-05-25**, producing 8 years of git history across 2913 problems.

Each problem gets its own Markdown file with:
- English original (assembled directly from JSON)
- Chinese translation (Ollama, 1 call)
- Step-by-step Python solution for beginners (Ollama, 1 call)

---

## Data Source

- **题目 JSON**：`leetcode_problems.json`，来源 [neenza/leetcode-problems](https://github.com/neenza/leetcode-problems)。仓库不内置该 JSON 文件，请大家自行下载 `merged_problems.json`，并按项目需要保存为 `leetcode_problems.json`。

Each problem JSON file contains the following fields:

- `title`: The name of the problem (e.g., "Container With Most Water").
- `problem_id`: The internal problem ID (string).
- `frontend_id`: The LeetCode frontend ID (string).
- `difficulty`: The difficulty level (Easy, Medium, or Hard).
- `problem_slug`: The URL-friendly name (e.g., container-with-most-water).
- `topics`: Array of topic tags (e.g., Array, Two Pointers).
- `description`: The full problem statement, usually in Markdown format.
- `examples`: Array of example objects, each with `example_num`, `example_text`, and `images`.
- `constraints`: Array of constraints or limits for the problem.
- `follow_ups`: Array of follow-up questions (if any).
- `hints`: Array of hints for solving the problem.
- `code_snippets`: Object containing starter code for various languages (e.g., python, cpp, java, etc.).
- `solutions`: HTML string containing editorial content for some problems.
- Some fields (like `solutions`, `images`, `follow_ups`) may be missing for certain problems.

---

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) running locally with `gpt-oss:120b` pulled

```bash
ollama pull gpt-oss:120b
ollama serve
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
# Process the next unfinished problem (auto-resume)
python main.py

# Process all remaining problems with a progress bar
python main.py --all

# Force a specific problem by index (0-based)
python main.py --index 0

# Dry run — print info without calling Ollama or writing files
python main.py --dry-run
```

---

## Output

```
solutions/
├── 2018/
│   ├── 20180604_1-two-sum.md
│   └── 20180605_2-add-two-numbers.md
├── ...
└── 2026/
    └── 20260525_3640-trionic-array-ii.md
```

Each commit is dated to the corresponding day with a randomised time between 08:00 and 23:30:

```
solve #1: Two Sum          2018-06-04T14:37:22
solve #2: Add Two Numbers  2018-06-05T09:12:55
...
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL` | `gpt-oss:120b` | Ollama model name |
| `OLLAMA_URL` | `http://10.54.79.119:11434/api/generate` | Ollama API endpoint (old: localhost) |
| `OLLAMA_TIMEOUT` | `300` | Request timeout in seconds |

---

## Docker

```bash
# Build
docker build -t daily-leetcode .

# Run (Ollama must be running on the host)
docker run --add-host=host.docker.internal:host-gateway \
  -v $(pwd)/solutions:/app/solutions \
  daily-leetcode
```

> On Linux add `--add-host=host.docker.internal:host-gateway` so the container can reach the host's Ollama.  
> On macOS / Windows `host.docker.internal` resolves automatically.

---

## Project Structure

```
├── config.py               Global config (env-overridable)
├── llm.py                  Ollama API wrapper
├── prompts.py              Translation & solution prompt builders
├── committer.py            git add + commit with historical dates
├── main.py                 Entry point
├── leetcode_problems.json  Source data (2913 problems, read-only)
└── solutions/              Generated Markdown files
```
