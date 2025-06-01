https://roadmap.sh/projects/expense-tracker

a simple expense tracker for managing finances. expenses can be added, viewed, updated, and deleted.

all expenses exist within a sqlite db

usage:

```bash
python3 main.py add --description 'babysitter' --amount 200 --category 'personal'
# expense added successfully (ID: 1)
```

```bash
python3 main.py update 1 --amount 20
# previous expense of 200 updated to 20 successfully (ID: 1)
```
