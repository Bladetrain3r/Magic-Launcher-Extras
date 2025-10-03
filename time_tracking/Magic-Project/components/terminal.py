from controller import ProjectController
from model import DataStore
from argparse import ArgumentParser
from typing import Optional

class TerminalInterface:

    def __init__(self, datastore: Optional[DataStore] = None):
        self.controller = ProjectController(datastore)  # Create instance
        self.parser = self._setup_parser()

    def _setup_parser(self) -> ArgumentParser:
        parser = ArgumentParser(description="Magic Project Terminal Interface")
        subparsers = parser.add_subparsers(dest='command')

        # Add subcommands
        subparsers.add_parser('list', help='List all projects')
        
        spark_parser = subparsers.add_parser('spark', help='Spark a project')
        spark_parser.add_argument('project', type=str, help='Project name')
        spark_parser.add_argument('note', type=str, help='Task note')
        spark_parser.add_argument('--priority', type=str, default='MEDIUM', help='Task priority')

        status_parser = subparsers.add_parser('status', help='Show project status')
        status_parser.add_argument('--limit', type=int, help='Limit number of projects shown')
        status_parser.add_argument('--include-frozen', action='store_true', help='Include frozen projects')

        complete_parser = subparsers.add_parser('complete', help='Complete a task')
        complete_parser.add_argument('project', type=str, help='Project name')
        complete_parser.add_argument('task_note', type=str, help='Task note (partial match allowed)')

        add_task_parser = subparsers.add_parser('add_task', help='Add a task to a project')
        add_task_parser.add_argument('project', type=str, help='Project name')
        add_task_parser.add_argument('note', type=str, help='Task note')
        add_task_parser.add_argument('--priority', type=str, default='MEDIUM', help='Task priority')

        freeze_parser = subparsers.add_parser('freeze', help='Freeze a project')
        freeze_parser.add_argument('project', type=str, help='Project name')

        unfreeze_parser = subparsers.add_parser('unfreeze', help='Unfreeze a project')
        unfreeze_parser.add_argument('project', type=str, help='Project name')

        subparsers.add_parser('heat', help='Show heat distribution of all projects')

        return parser

    def run(self, args: Optional[list] = None):
        args = self.parser.parse_args(args)
        
        if args.command == 'list':
            # Use status() method to get formatted project list
            projects = self.controller.status(include_frozen=True)
            for project in projects:
                task_count = project.get('active_tasks', 0)
                print(f"{project['name']} - {project['state']} - {task_count} tasks")
        
        elif args.command == 'spark':
            project = self.controller.spark(args.project, args.note, args.priority)
            print(f"Sparked project '{args.project}' with task: {args.note}")
        
        elif args.command == 'status':
            projects = self.controller.status(
                limit=args.limit, 
                include_frozen=args.include_frozen
            )
            for project in projects:
                active_tasks = project.get('active_tasks', 0)
                completed_tasks = project.get('completed_tasks', 0)
                heat_score = project.get('heat_score', 0)
                print(f"{project['name']}: {project['state']} "
                      f"({active_tasks} active, {completed_tasks} done) "
                      f"heat: {heat_score:.1f}")
        
        elif args.command == 'complete':
            task = self.controller.complete_task(args.project, args.task_note)
            print(f"Completed task in project '{args.project}': {task['note']}")
        
        elif args.command == 'add_task':
            task = self.controller.add_task(args.project, args.note, args.priority)
            print(f"Added task to project '{args.project}': {task['note']}")
        
        elif args.command == 'freeze':
            project = self.controller.freeze_project(args.project)
            print(f"Froze project '{args.project}'")
        
        elif args.command == 'unfreeze':
            project = self.controller.unfreeze_project(args.project)
            print(f"Unfroze project '{args.project}' - now {project['state']}")
        
        elif args.command == 'heat':
            distribution = self.controller.get_heat_distribution()
            print("Heat distribution:")
            for state, count in distribution.items():
                print(f"  {state}: {count} projects")
        
        else:
            self.parser.print_help()

def main():
    interface = TerminalInterface()
    interface.run()

if __name__ == "__main__":
    main()