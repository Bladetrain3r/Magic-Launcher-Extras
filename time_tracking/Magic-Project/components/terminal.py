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
        list_parser = subparsers.add_parser('list', help='List all projects')
        list_parser.add_argument('--show-frozen', action='store_true', help='Show frozen projects')

        spark_parser = subparsers.add_parser('spark', help='Spark a project')
        spark_parser.add_argument('project', type=str, help='Project name')
        spark_parser.add_argument('note', type=str, help='Task note')
        spark_parser.add_argument('--priority', type=str, default='MEDIUM', help='Task priority')

        status_parser = subparsers.add_parser('status', help='Show detailed status for a specific project')
        status_parser.add_argument('-n', '--index', type=int, help='Project index (0-based)')
        status_parser.add_argument('project', type=str, nargs='?', help='Project name')
        status_parser.add_argument('--show-tasks', action='store_true', help='Show all tasks for the project')

        complete_parser = subparsers.add_parser('complete', help='Complete a task')
        complete_parser.add_argument('project', type=str, help='Project name')
        complete_parser.add_argument('task_note', type=str, help='Task note (partial match allowed)')
        complete_parser.add_argument('--declined', action='store_true', help='Mark the task as declined')

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
            projects = self.controller.status(include_frozen=args.show_frozen)
            if not projects:
                print("No projects found.")
            else:
                i = 0
                for project in projects:
                    task_count = project.get('active_tasks', 0)
                    print(f"{i}: {project['name']} - {project['state']} - {task_count} tasks")
                    i += 1

        elif args.command == 'spark':
            project = self.controller.spark(args.project, args.note, args.priority)
            print(f"Sparked project '{args.project}' with task: {args.note}")
        
        elif args.command == 'status':
            if args.index is not None:
                project_name = self.controller.get_project_by_index(args.index)
                if not project_name:
                    print(f"Error: Index {args.index} out of range. Use 'mp list' to see available indices.")
                    return
            elif args.project:
                project_name = args.project
            else:
                print("Error: Must specify either project name or index.")
                return

            project = self.controller.get_project_status(project_name)
            if project:
                active_tasks = project.get('active_tasks', 0)
                completed_tasks = project.get('completed_tasks', 0)
                heat_score = project.get('heat_score', 0)
                print(f"{project['name']}: {project['state']} "
                      f"({active_tasks} active, {completed_tasks} done) "
                      f"heat: {heat_score:.1f}")
                
                if args.show_tasks:
                    tasks = project.get('tasks', [])
                    if tasks:
                        print("Tasks:")
                        for task in tasks:
                            if task.get('state') == 'completed':
                                status = "✓"
                            elif task.get('state') == 'declined':
                                status = "✗"
                            else:
                                status = "○"
                            print(f"  {status} {task['note']} [{task.get('priority', 'MEDIUM')}]")
                    else:
                        print("No tasks found.")
            else:
                print(f"Project '{args.project}' not found")
        
        elif args.command == 'complete':
            task = self.controller.complete_task(args.project, args.task_note, args.declined)
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