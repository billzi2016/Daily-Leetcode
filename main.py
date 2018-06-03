import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

from tqdm import tqdm

from config import DATA_FILE, SOLUTIONS_DIR, START_DATE
import llm
from prompts import translation_prompt, solution_prompt
from committer import commit_file

DIFFICULTY_ZH = {"Easy": "简单", "Medium": "中等", "Hard": "困难"}


def load_problems() -> list:
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)["questions"]


def count_done() -> int:
    base = Path(SOLUTIONS_DIR)
    if not base.exists():
        return 0
    return sum(1 for _ in base.rglob("*.md"))


def commit_date(index: int) -> str:
    base = datetime.strptime(START_DATE, "%Y-%m-%d")
    return (base + timedelta(days=index)).strftime("%Y-%m-%d")


def out_path(date_str: str, frontend_id: str, problem_slug: str) -> Path:
    yyyy = date_str[:4]
    yyyymmdd = date_str.replace("-", "")
    return Path(SOLUTIONS_DIR) / yyyy / f"{yyyymmdd}_{frontend_id}-{problem_slug}.md"


def clean_description(desc: str) -> str:
    lines = [
        l for l in desc.split("\n")
        if not re.match(r"^(Example \d+:|Constraints:)\s*$", l)
    ]
    return "\n".join(lines).strip()


def build_english_section(problem: dict) -> str:
    desc = clean_description(problem.get("description", ""))

    example_blocks = []
    for ex in problem.get("examples", []):
        example_blocks.append(
            f"**Example {ex['example_num']}:**\n\n```\n{ex['example_text'].strip()}\n```"
        )

    constraints = problem.get("constraints", [])
    constraints_text = "\n".join(f"- {c}" for c in constraints)

    parts = [f"## 题目（英文原版）\n\n**Description**\n\n{desc}"]
    if example_blocks:
        parts.append("**Examples**\n\n" + "\n\n".join(example_blocks))
    if constraints_text:
        parts.append(f"**Constraints**\n\n{constraints_text}")

    return "\n\n".join(parts)


def build_markdown(
    problem: dict,
    chinese_title: str,
    english_section: str,
    translation_body: str,
    solution: str,
) -> str:
    fid = problem["frontend_id"]
    title = problem["title"]
    diff = DIFFICULTY_ZH.get(problem.get("difficulty", ""), problem.get("difficulty", ""))
    topics = "、".join(problem.get("topics", []))
    slug = problem["problem_slug"]

    header = (
        f"# #{fid}. {chinese_title} / {title}\n\n"
        f"> 难度：{diff} · 标签：{topics} · "
        f"[LeetCode 链接](https://leetcode.com/problems/{slug}/)"
    )
    chinese_section = f"## 题目（中文翻译）\n\n{translation_body.strip()}"
    solution_clean = re.sub(r"^\s*-{3,}\s*\n", "", solution.strip())

    return "\n\n---\n\n".join([header, english_section, chinese_section, solution_clean])


def process_one(index: int, problems: list, dry_run: bool = False, pbar: tqdm = None) -> bool:
    if index >= len(problems):
        print(f"[INFO] 所有 {len(problems)} 题已处理完毕")
        return False

    problem = problems[index]
    date_str = commit_date(index)
    fid = problem["frontend_id"]
    title = problem["title"]
    path = out_path(date_str, fid, problem["problem_slug"])

    def _desc(msg: str):
        if pbar:
            pbar.set_description(f"#{fid} {msg}")

    if path.exists():
        if pbar:
            pbar.write(f"[SKIP] 已存在: {path}")
        else:
            print(f"[SKIP] 已存在: {path}")
        return True

    _desc("翻译中...")
    if dry_run:
        if pbar:
            pbar.write(f"[DRY-RUN] #{fid} {title} → {path}")
        else:
            print(f"[DRY-RUN] #{fid} {title} → {path}")
        return True

    # Ollama call 1: translation
    t_raw = llm.generate(translation_prompt(problem))
    lines = t_raw.strip().split("\n")
    chinese_title = lines[0].strip().lstrip("#").strip() if lines else title
    translation_body = "\n".join(lines[1:]).strip() if len(lines) > 1 else t_raw.strip()

    # Ollama call 2: solution
    _desc("生成题解...")
    solution = llm.generate(solution_prompt(problem))

    # Assemble markdown
    _desc("写入文件...")
    english_section = build_english_section(problem)
    md = build_markdown(problem, chinese_title, english_section, translation_body, solution)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(md, encoding="utf-8")

    # Commit
    _desc("提交 git...")
    commit_file(str(path), fid, title, date_str)

    if pbar:
        pbar.write(f"[OK] #{fid} {title} → {path}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Daily LeetCode 生成器")
    parser.add_argument("--all", action="store_true", help="批量处理所有未完成的题目")
    parser.add_argument("--index", type=int, default=None, help="强制处理指定索引的题目")
    parser.add_argument("--dry-run", action="store_true", help="只打印，不调用 LLM，不写文件")
    args = parser.parse_args()

    problems = load_problems()

    if args.index is not None:
        process_one(args.index, problems, dry_run=args.dry_run)
        return

    start = count_done()

    if args.all:
        remaining = len(problems) - start
        with tqdm(total=remaining, initial=0, unit="题", dynamic_ncols=True) as pbar:
            for i in range(start, len(problems)):
                if not process_one(i, problems, dry_run=args.dry_run, pbar=pbar):
                    break
                pbar.update(1)
    else:
        process_one(start, problems, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
