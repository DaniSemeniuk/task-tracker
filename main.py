"""Main script"""

import argparse
import json
import sys
import args_functions


def main(args):
    # basic data structure
    data = {"count": 1, "tasks": {}}

    # loading or creating JSON data base
    try:
        with open("DB.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        with open("DB.json", "x", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # ADD funcionality
    if args.add:
        args_functions.add(data, args)
        sys.exit()

    # LIST funcionality
    if args.list:
        args_functions.display(data, args)
        sys.exit()

    # UPDATE funcionality
    if args.update:
        args_functions.update(data, args)
        sys.exit()


if __name__ == "__main__":
    # creation of argument parser
    parser = argparse.ArgumentParser(description="task manager in JSON file")

    # add exclusive arguments
    exclusive_args = parser.add_mutually_exclusive_group()
    exclusive_args.add_argument("--add", help="add a new task: add 'task'[str]")
    exclusive_args.add_argument(
        "--update",
        nargs=2,
        help="update an existing task: update id[int] 'new task'[str]",
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
    main(parser.parse_args())
