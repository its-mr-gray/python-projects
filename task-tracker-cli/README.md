- https://roadmap.sh/projects/task-tracker
- a simple CLI for setting up a tracking tasks. tasks can be added, removed, and moved to different statuses. some examples:

```bash
python3 main.py -h
# displays description of the task tracker. the -h flag can also be used on any command passed to the CLI for a description of available commands.
```

```bash
python3 main.py list-all
#lists all tasks
```

```bash
python3 main.py add "take out the trash"
#adds a new task in the TODO status
```

```bash
python3 main.py update-status "take out the trash" "TODO" "IN PROGRESS"
#moves the specified task from its current status to a given status
```
