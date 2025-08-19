"""functions for the CLI arguments"""

import json
import os
from datetime import datetime


def dump(data, filename="DB.json"):
    temp_file = filename + ".tmp"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(temp_file, filename)  # reemplaza atómicamente el archivo
    except Exception as e:
        if os.path.exists(temp_file):
            os.remove(temp_file)  # borramos el temporal si algo falló
        raise e


def add(data, args):
    data["tasks"][str(data["count"])] = {
        "description": args.add,
        "status": "to-do",
        "createdAt": datetime.now().isoformat(),
        "updateAt": datetime.now().isoformat(),
    }
    data["count"] += 1
    dump(data)


def display(data, args):
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
        print("There is no tasks :(")
    else:
        for task in listing:
            print(task)


def update(data, args):
    task_id = args.update[0]
    task_desc = args.update[1]
    if not task_id.isnumeric():
        raise ValueError("Usage: --update id[int] new_task[str]")

    try:
        data["tasks"][task_id]["description"] = task_desc
        data["tasks"][task_id]["updateAt"] = datetime.now().isoformat()
        dump(data)
    except KeyError:
        print("That id doesn't exist")
