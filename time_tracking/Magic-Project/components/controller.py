from model import DataStore, PROJECT_TEMPLATE, TASK_TEMPLATE, new_project, new_task, sanitize_project_id
from typing import Optional, Dict, Any
from datetime import datetime
from typing import List

class ProjectController:
    """Controller for managing projects and tasks"""

    HEAT_THRESHOLDS = {
        'hot': 2,      # Modified within 2 days
        'warm': 7,     # Modified within 7 days  
        'cold': 30,    # Modified within 30 days
        'frozen': 90   # Older than 90 days
    }

    def __init__(self, datastore: Optional[DataStore] = None):
        self.datastore = datastore or DataStore()
        self.data = self.load_data()

    # Internal Helpers

    def _recalculate_all_states(self, data: Dict):
        """Recalculate heat states for all projects"""
        for project in data['projects'].values():
            project['state'] = self._calculate_heat(project['record_modified'])
    
    def _count_active_tasks(self, tasks: Dict) -> int:
        """Count tasks that aren't completed"""
        return sum(1 for task in tasks.values() if task['completed'] is None)
    
    def _count_completed_tasks(self, tasks: Dict) -> int:
        """Count completed tasks"""
        return sum(1 for task in tasks.values() if task['completed'] is not None)

    def _calculate_heat(self, last_modified: str) -> str:
        """Calculate project heat based on last modification time"""
        try:
            modified_dt = datetime.fromisoformat(last_modified)
            days_ago = (datetime.now() - modified_dt).days
            
            if days_ago <= self.HEAT_THRESHOLDS['hot']:
                return 'hot'
            elif days_ago <= self.HEAT_THRESHOLDS['warm']:
                return 'warm'
            elif days_ago <= self.HEAT_THRESHOLDS['cold']:
                return 'cold'
            else:
                return 'frozen'
        except (ValueError, TypeError):
            return 'cold'  # Default for invalid dates
    
    def _get_heat_score(self, last_modified: str) -> float:
        """Get numerical heat score for sorting (higher = hotter)"""
        try:
            modified_dt = datetime.fromisoformat(last_modified)
            days_ago = (datetime.now() - modified_dt).days
            
            # Exponential decay - more recent = much higher score
            return max(0, 100 * (0.9 ** days_ago))
        except (ValueError, TypeError):
            return 0
        
    # Public Methods
        
    def load_data(self) -> Dict:
        """Load and refresh project states"""
        data = self.datastore.load()
        self._recalculate_all_states(data)
        return data    
    
    def spark(self, project_name: str, task_note: str = "", priority: str = "MEDIUM") -> Dict:
        """
        Create or update project, add task if provided, push to top of stack
        This is the core ADHD-friendly "capture everything NOW" method
        """
        data = self.load_data()
        project_id = sanitize_project_id(project_name)
        
        # Create or update project
        if project_id not in data['projects']:
            data['projects'][project_id] = new_project(project_name, priority)
        else:
            # Update existing project
            data['projects'][project_id]['record_modified'] = datetime.now().isoformat()
            # Boost priority if we're re-engaging
            if data['projects'][project_id]['priority'] == 'LOW':
                data['projects'][project_id]['priority'] = 'MEDIUM'
        
        # Add task if provided
        if task_note.strip():
            task = new_task(task_note, priority)
            task_id = task['uuid']  # Use the UUID as the key
            data['projects'][project_id]['tasks'][task_id] = task
        
        # Stack management - move to top
        if project_id in data['stack']:
            data['stack'].remove(project_id)
        data['stack'].insert(0, project_id)
        
        # Recalculate state
        data['projects'][project_id]['state'] = self._calculate_heat(
            data['projects'][project_id]['record_modified']
        )
        
        self.datastore.save(data)
        return data['projects'][project_id]

    def status(self, limit: Optional[int] = None, include_frozen: bool = False) -> List[Dict]:
        """
        Get projects in stack order with calculated states and task counts
        """
        data = self.load_data()
        result = []
        
        stack_projects = data['stack'][:limit] if limit else data['stack']
        
        for project_id in stack_projects:
            if project_id not in data['projects']:
                continue  # Skip orphaned stack entries
            
            project = data['projects'][project_id].copy()
            
            # Skip frozen projects unless explicitly requested
            if project['state'] == 'frozen' and not include_frozen:
                continue
            
            # Add computed fields
            project['active_tasks'] = self._count_active_tasks(project['tasks'])
            project['completed_tasks'] = self._count_completed_tasks(project['tasks'])
            project['heat_score'] = self._get_heat_score(project['record_modified'])
            
            result.append(project)
        
        return result

    def complete_task(self, project_name: str, task_partial: str) -> Dict:
        """
        Mark task as completed by partial text match
        Updates project heat when task completed
        """
        data = self.load_data()
        project_id = sanitize_project_id(project_name)
        
        if project_id not in data['projects']:
            raise ValueError(f"Project '{project_name}' not found")
        
        project = data['projects'][project_id]
        
        # Find task by partial match
        matching_tasks = [
            (task_id, task) for task_id, task in project['tasks'].items()
            if task_partial.lower() in task['note'].lower() and task['completed'] is None
        ]
        
        if not matching_tasks:
            raise ValueError(f"No active task found matching '{task_partial}'")
        
        if len(matching_tasks) > 1:
            raise ValueError(f"Multiple tasks match '{task_partial}', be more specific")
        
        task_id, task = matching_tasks[0]  # Fixed: unpack the tuple properly
        
        # Complete the task
        task['completed'] = datetime.now().isoformat()
        task['state'] = 'completed'
        
        # Update project heat
        project['record_modified'] = datetime.now().isoformat()
        project['state'] = self._calculate_heat(project['record_modified'])
        
        self.datastore.save(data)
        return task    
    
    def add_task(self, project_name: str, note: str, priority: str = "MEDIUM") -> Dict:
        """Add task to existing project"""
        data = self.load_data()
        project_id = sanitize_project_id(project_name)
        
        if project_id not in data['projects']:
            raise ValueError(f"Project '{project_name}' not found")
        
        task = new_task(note, priority) 
        task_id = task['uuid']
        data['projects'][project_id]['tasks'][task_id] = task
    
        # Update project heat
        data['projects'][project_id]['record_modified'] = datetime.now().isoformat()
        data['projects'][project_id]['state'] = self._calculate_heat(
            data['projects'][project_id]['record_modified']
        )
        
        self.datastore.save(data)
        return task

    def freeze_project(self, project_name: str) -> Dict:
        """Move project to frozen state (archived but not deleted)"""
        data = self.load_data()
        project_id = sanitize_project_id(project_name)
        
        if project_id not in data['projects']:
            raise ValueError(f"Project '{project_name}' not found")
        
        project = data['projects'][project_id]
        project['state'] = 'frozen'
        
        # Move to end of stack
        if project_id in data['stack']:
            data['stack'].remove(project_id)
            data['stack'].append(project_id)
        
        self.datastore.save(data)
        return project

    def get_project_status(self, project_name: str) -> Optional[Dict]:
        """
        Get detailed status for a specific project including tasks
        """
        data = self.load_data()
        project_id = sanitize_project_id(project_name)
        
        if project_id not in data['projects']:
            return None
        
        project = data['projects'][project_id].copy()
        
        # Add computed fields
        project['active_tasks'] = self._count_active_tasks(project['tasks'])
        project['completed_tasks'] = self._count_completed_tasks(project['tasks'])
        project['heat_score'] = self._get_heat_score(project['record_modified'])
        
        # Convert tasks dict to list for easier iteration in terminal
        project['tasks'] = list(project['tasks'].values())
        
        return project

    def unfreeze_project(self, project_name: str) -> Dict:
        """Bring project back from frozen state"""
        data = self.load_data()
        project_id = sanitize_project_id(project_name)
        
        if project_id not in data['projects']:
            raise ValueError(f"Project '{project_name}' not found")
        
        project = data['projects'][project_id]
        project['record_modified'] = datetime.now().isoformat()
        project['state'] = self._calculate_heat(project['record_modified'])
        
        # Move to top of stack
        if project_id in data['stack']:
            data['stack'].remove(project_id)
        data['stack'].insert(0, project_id)
        
        self.datastore.save(data)
        return project

    def get_heat_distribution(self) -> Dict[str, int]:
        """Get count of projects in each heat state"""
        data = self.load_data()
        distribution = {'hot': 0, 'warm': 0, 'cold': 0, 'frozen': 0}
        
        for project in data['projects'].values():
            state = project.get('state', 'cold')
            distribution[state] = distribution.get(state, 0) + 1
        
        return distribution
    
