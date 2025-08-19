import argparse
import json
from datetime import datetime


# creation of argument parser
parser = argparse.ArgumentParser(description="task manager in JSON file")

# add exclusive arguments
exclusive_args = parser.add_mutually_exclusive_group()
exclusive_args.add_argument("--add", help="add a new task: add 'task'[str]")
exclusive_args.add_argument(
    "--update", nargs=2, help="update an existing task: update id[int] 'new task'[str]"
)
exclusive_args.add_argument("--delete", help="delete a task: delete id[int]")
exclusive_args.add_argument(
    "--list",
    choices=["all", "done", "to-do", "in-progress"],
    help="list tasks: list 'all'/'done'/'to-do'/'in-progress'[str]",
)
exclusive_args.add_argument(
    "--mark",
    choices=["in-progress", "done", "to-do"],
    help="change task status: mark 'status'[str]",
)

# parse arguments
args = parser.parse_args()
# print(args)

# basic data structure
data = {"count": 1, "tasks": {}}

# loading or creating JSON data base
try:
    with open("DB.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError as e:
    with open("DB.json", "x", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ADD funcionality
if args.add:
    data["tasks"][str(data["count"])] = {
        "description": args.add,
        "status": "to-do",
        "createdAt": datetime.now().isoformat(),
        "updateAt": datetime.now().isoformat(),
    }
    data["count"] += 1
    with open("DB.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)
    exit(1)

# LIST funcionality
if args.list:
    listing = []
    for key_id, task in data["tasks"].items():
        if args.list in (task["status"], "all"):
            listing.append(
                f"ID: {key_id}\n"
                f"Description: {task['description']}\n"
                f"Status: {task['status']}\n"
                f"Created at: {datetime.fromisoformat(task['createdAt']).strftime('%d-%m-%Y %H:%M:%S')}\n"
                f"Updated at: {datetime.fromisoformat(task['updateAt']).strftime('%d-%m-%Y %H:%M:%S')}\n\n"
            )
    if not listing:
        print("There is no tasks with that status :(")
    else:
        for task in listing:
            print(task)
    exit(1)

# UPDATE funcionality
if args.update:
    task_id = args.update[0]
    task_desc = args.update[1]
    if not task_id.isnumeric():
        raise ValueError("Usage: --update id[int] new_task[str]")

    try:
        data["tasks"][task_id]["description"] = task_desc
        data["tasks"][task_id]["updateAt"] = datetime.now().isoformat()
        with open("DB.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)
    except KeyError:
        print("That id doesn't exist")
        exit(1)
