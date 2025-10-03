# MagicProjects - Pattern-Based Project & Task Tracker
# Complete Implementation Blueprint v1.0

"""
IMPLEMENTATION PLAN
===================

Phase 1: Core Data Layer (START HERE)
- JSON file operations with atomic writes
- Project/Task CRUD operations
- Stack management
- Timestamp handling (file_modified vs record_modified)

Phase 2: Basic Commands
- spark: Quick project/task capture
- status: Visual stack display
- tasks: List tasks for project
- next: Get next actionable task

Phase 3: State Management
- Auto-calculate hot/warm/cold from timestamps
- Priority handling (LOW/MEDIUM/HIGH)
- Task completion tracking

Phase 4: Polish
- Color output (ANSI codes)
- Better error handling
- Help system
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import fcntl  # For file locking on Unix
import sys

# =============================================================================
# CONFIGURATION
# =============================================================================

DATA_DIR = Path.home() / '.magicprojects'
PROJECTS_FILE = DATA_DIR / 'projects.json'

# State thresholds (days)
PROJECT_THRESHOLDS = {
    'hot': 3,
    'warm': 7,
    'cold': 30
}

TASK_THRESHOLDS = {
    'new': 1,
    'active': 3,
    'stale': 7
}

# ANSI color codes
COLORS = {
    'hot': '\033[92m',      # bright green
    'warm': '\033[93m',     # yellow
    'cold': '\033[96m',     # cyan
    'frozen': '\033[90m',   # gray
    'high': '\033[91m',     # red
    'medium': '\033[97m',   # white
    'low': '\033[37m',      # dim white
    'reset': '\033[0m'
}

# =============================================================================
# DATA STRUCTURE
# =============================================================================

DEFAULT_DATA = {
    "projects": {},
    "stack": []
}

PROJECT_TEMPLATE = {
    "name": "",
    "priority": "MEDIUM",
    "created": "",
    "file_modified": None,  # For future filesystem watching
    "record_modified": "",
    "state": "hot",
    "tags": [],
    "related": [],
    "tasks": {}
}

TASK_TEMPLATE = {
    "note": "",
    "priority": "MEDIUM",
    "created": "",
    "completed": None,
    "state": "new"
}

# =============================================================================
# FILE OPERATIONS
# =============================================================================

class DataStore:
    """Handle atomic file operations with locking"""
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self._ensure_file()
    
    def _ensure_file(self):
        """Create data file if it doesn't exist"""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            with open(self.filepath, 'w') as f:
                json.dump(DEFAULT_DATA, f, indent=2)
    
    def load(self) -> Dict:
        """Load data with file locking"""
        with open(self.filepath, 'r') as f:
            if sys.platform != 'win32':
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            try:
                return json.load(f)
            finally:
                if sys.platform != 'win32':
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    
    def save(self, data: Dict):
        """Save data atomically with file locking"""
        # Write to temp file first
        temp_file = self.filepath.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            if sys.platform != 'win32':
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            finally:
                if sys.platform != 'win32':
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        
        # Atomic rename
        temp_file.replace(self.filepath)

# =============================================================================
# CORE LOGIC
# =============================================================================

class MagicProjects:
    """Main project tracker logic"""
    
    def __init__(self, datastore: DataStore):
        self.store = datastore
    
    def _now(self) -> str:
        """Get current ISO timestamp"""
        return datetime.now().isoformat()
    
    def _calculate_state(self, timestamp_str: str, thresholds: Dict) -> str:
        """Calculate hot/warm/cold state from timestamp"""
        if not timestamp_str:
            return 'frozen'
        
        timestamp = datetime.fromisoformat(timestamp_str)
        age_days = (datetime.now() - timestamp).days
        
        if age_days < thresholds['hot']:
            return 'hot'
        elif age_days < thresholds['warm']:
            return 'warm'
        elif age_days < thresholds.get('cold', float('inf')):
            return 'cold'
        else:
            return 'frozen'
    
    def spark(self, project_name: str, note: str, priority: str = "MEDIUM") -> Dict:
        """
        Quick capture - create/update project and push to top of stack
        
        Returns: Updated project data
        """
        data = self.store.load()
        project_id = project_name.lower().replace(' ', '_')
        
        # Create or update project
        if project_id not in data['projects']:
            project = PROJECT_TEMPLATE.copy()
            project['name'] = project_name
            project['priority'] = priority.upper()
            project['created'] = self._now()
            project['record_modified'] = self._now()
            project['tasks'] = {}
            data['projects'][project_id] = project
        else:
            data['projects'][project_id]['record_modified'] = self._now()
        
        # Add as task if it looks like task note
        if len(note) > 10:  # Arbitrary threshold
            task_id = f"task_{len(data['projects'][project_id]['tasks'])}"
            task = TASK_TEMPLATE.copy()
            task['note'] = note
            task['priority'] = priority.upper()
            task['created'] = self._now()
            data['projects'][project_id]['tasks'][task_id] = task
        
        # Push to top of stack
        if project_id in data['stack']:
            data['stack'].remove(project_id)
        data['stack'].insert(0, project_id)
        
        # Update state
        data['projects'][project_id]['state'] = 'hot'
        
        self.store.save(data)
        return data['projects'][project_id]
    
    def status(self) -> List[Dict]:
        """
        Get stack visualization data
        
        Returns: List of projects with computed states
        """
        data = self.store.load()
        result = []
        
        for project_id in data['stack']:
            if project_id not in data['projects']:
                continue
            
            project = data['projects'][project_id].copy()
            
            # Recalculate state
            project['state'] = self._calculate_state(
                project['record_modified'],
                PROJECT_THRESHOLDS
            )
            
            # Count active tasks
            active_tasks = sum(
                1 for t in project['tasks'].values()
                if t['completed'] is None
            )
            project['active_task_count'] = active_tasks
            
            result.append(project)
        
        return result
    
    def add_task(self, project_name: str, note: str, priority: str = "MEDIUM") -> Dict:
        """Add task to project"""
        data = self.store.load()
        project_id = project_name.lower().replace(' ', '_')
        
        if project_id not in data['projects']:
            raise ValueError(f"Project '{project_name}' not found")
        
        task_id = f"task_{len(data['projects'][project_id]['tasks'])}"
        task = TASK_TEMPLATE.copy()
        task['note'] = note
        task['priority'] = priority.upper()
        task['created'] = self._now()
        
        data['projects'][project_id]['tasks'][task_id] = task
        data['projects'][project_id]['record_modified'] = self._now()
        
        self.store.save(data)
        return task

# =============================================================================
# CLI INTERFACE (Basic implementation)
# =============================================================================

def format_project_line(project: Dict) -> str:
    """Format a project for status display"""
    state = project['state']
    priority = project['priority']
    name = project['name']
    task_count = project.get('active_task_count', 0)
    
    # State indicator
    indicators = {
        'hot': '●',
        'warm': '◐',
        'cold': '○',
        'frozen': '·'
    }
    indicator = indicators.get(state, '?')
    
    # Color codes
    state_color = COLORS.get(state, '')
    priority_color = COLORS.get(priority.lower(), '')
    reset = COLORS['reset']
    
    task_info = f" ({task_count} tasks)" if task_count > 0 else ""
    
    return f"{state_color}{indicator}{reset} {name} {priority_color}[{priority}]{reset}{task_info}"

def cmd_spark(args):
    """Handle spark command"""
    mp = MagicProjects(DataStore(PROJECTS_FILE))
    project = mp.spark(args.project, args.note, args.priority)
    print(f"✓ Sparked: {project['name']}")

def cmd_status(args):
    """Handle status command"""
    mp = MagicProjects(DataStore(PROJECTS_FILE))
    projects = mp.status()
    
    if not projects:
        print("No projects yet. Use 'mp spark <project> <note>' to start.")
        return
    
    print("┌─ STACK " + "─" * 40 + "┐")
    for project in projects:
        print(f"│ {format_project_line(project)}")
    print("└─" + "─" * 47 + "┘")

# =============================================================================
# NEXT STEPS
# =============================================================================

"""
TODO for full implementation:

1. Complete CLI with argparse
   - All commands from architecture doc
   - Help system
   - Error handling

2. Task management
   - Complete tasks
   - List tasks by project
   - Next actionable task across all projects

3. Advanced features
   - File watching for file_modified timestamps
   - Grep/search functionality
   - Stats display
   - Export functionality

4. Integration
   - Daily notes linking
   - Resonance DB queries
   - Context preservation

5. GUI (Phase 4)
   - Tkinter interface
   - CGA aesthetic
   - Visual stack display
"""