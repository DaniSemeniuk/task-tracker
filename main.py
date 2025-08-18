import argparse
import json
from datetime import datetime


###creation of exclusive CLI commands###
parser = argparse.ArgumentParser(description="task manager in JSON file")
exclusive_args = parser.add_mutually_exclusive_group()
exclusive_args.add_argument("--add", help="add a new task: add 'task'[str]")
exclusive_args.add_argument(
    "--update", nargs=2, help="update an existing task: update id[int] 'new task'[str]"
)
exclusive_args.add_argument("--delete", help="delete a task: delete id[int]")
exclusive_args.add_argument(
    "--list",
    choices=[None, "done", "todo", "in-progress"],
    help="list tasks: list 'done'/'todo'/'in-progress'[str] | None",
)
exclusive_args.add_argument(
    "--mark",
    choices=["in-progress", "done", "to-do"],
    help="change task status: mark 'status'[str]",
)
###parsin arguments###
args = parser.parse_args()


data = {"count": 1, "tasks": {}}

try:
    with open("DB.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        print(data)
except FileNotFoundError as e:
    with open("DB.json", "x", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if args.add:
    data["tasks"][data["count"]] = {
        "description": args.add,
        "status": "to-do",
        "createdAt": datetime.now().isoformat(),
        "updateAt": datetime.now().isoformat(),
    }
    data["count"] += 1
    print(json.dumps(data, indent=4, ensure_ascii=False))
    with open("DB.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
