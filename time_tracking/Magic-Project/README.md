# Magic-LauncherProject (Magic Projects)
## A simple stack based project manager

## Quick Setup
- Make sure you have Python installed
- python MLProject.py <command>

### Set up a permanent alias in BASH
```bash
# In this folder
echo "alias mp=\"python3 $(pwd)/MLProject.py\"" >> ~/.bash_aliases
```

### Permanent Function in Powershell
```powershell
# mp is already a system alias for Move-ItemProperty and I refuse to use the other acronym.
echo "function MagicProject {python $pwd\MLProject.py}" >> $profile && . $profile
```

## Using the App

```
Magic Project Terminal Interface

positional arguments:
  {list,spark,status,complete,add_task,freeze,unfreeze,heat}
    list                List all projects
    spark               Spark a project
    status              Show detailed status for a specific project
    complete            Complete a task
    add_task            Add a task to a project
    freeze              Freeze a project
    unfreeze            Unfreeze a project
    heat                Show heat distribution of all projects

options:
  -h, --help            show this help message and exit
```

Example Commands:

```bash
# Create a project and task
mp spark "New Idea" "Write it down"
```

```bash
mp status "New Idea" --show-tasks
# Get status by list index
mp status -n 0 --show-tasks
```

```bash
# Complete a task - partial match supported, but must be unique.
mp complete "New Idea" "Write it"
# Or decline a task
mp complete "New Idea" "Write it" --decline
```

