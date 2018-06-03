import os
import random
import subprocess
import sys
from datetime import datetime, timedelta


def random_commit_time(date_str: str) -> str:
    base = datetime.strptime(date_str, "%Y-%m-%d")
    minutes = random.randint(8 * 60, 23 * 60 + 30)
    dt = base + timedelta(minutes=minutes)
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def commit_file(file_path: str, frontend_id: str, title: str, date_str: str) -> None:
    dt = random_commit_time(date_str)
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = dt
    env["GIT_COMMITTER_DATE"] = dt

    subprocess.run(["git", "add", file_path], check=True)
    subprocess.run(
        ["git", "commit", "-m", f"solve #{frontend_id}: {title}"],
        env=env,
        check=True,
    )
    print(f"  → committed: solve #{frontend_id}: {title}  [{dt}]")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("用法: python committer.py <file_path> <frontend_id> <title> <date_YYYY-MM-DD>")
        sys.exit(1)
    commit_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
