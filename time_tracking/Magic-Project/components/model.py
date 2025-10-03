# model.py - Data layer for MagicProjects
# Handles JSON storage, file locking, and data structure

import json
import re
import os
import sys
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
if sys.platform != 'win32':
    import fcntl
else:
    fcntl = None

# Default storage location
DATA_DIR = Path.home() / '.magicprojects'
PROJECTS_FILE = DATA_DIR / 'projects.json'

# Data templates
DEFAULT_DATA = {
    "projects": {},
    "stack": []
}

PROJECT_TEMPLATE = {
    "uuid": "",
    "name": "",
    "priority": "MEDIUM",
    "created": "",
    "file_modified": None,
    "record_modified": "",
    "state": "hot",
    "tags": [],
    "related": [],
    "tasks": {}
}

TASK_TEMPLATE = {
    "uuid": "",
    "note": "",
    "priority": "MEDIUM",
    "created": "",
    "completed": None,
    "state": "new"
}


class DataStore:
    """Handle atomic file operations with locking"""
    
    def __init__(self, filepath: Optional[Path] = None):
        self.filepath = filepath or PROJECTS_FILE
        self._ensure_file()
    
    def _ensure_file(self):
        """Create data directory and file if they don't exist"""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            with open(self.filepath, 'w') as f:
                json.dump(DEFAULT_DATA, f, indent=2)
    
    def load(self) -> Dict:
        """Load data with file locking (Unix only)"""
        try:
            with open(self.filepath, 'r') as f:
                if sys.platform != 'win32':
                    fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                try:
                    data = json.load(f)
                    # Ensure required keys exist
                    if 'projects' not in data:
                        data['projects'] = {}
                    if 'stack' not in data:
                        data['stack'] = []
                    return data
                finally:
                    if sys.platform != 'win32':
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except (json.JSONDecodeError, FileNotFoundError):
            return DEFAULT_DATA.copy()
    
    def save(self, data: Dict):
        """Save data atomically with file locking"""
        # Write to temp file first for atomic operation
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
    
    def backup(self, suffix: Optional[str] = None):
        """Create backup of current data"""
        if not self.filepath.exists():
            return None
        
        if suffix is None:
            suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        backup_file = self.filepath.with_suffix(f'.backup.{suffix}')
        data = self.load()
        
        with open(backup_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return backup_file


# Utility functions for template creation
def new_project(name: str, priority: str = "MEDIUM") -> Dict:
    """Create new project dict from template"""
    project = PROJECT_TEMPLATE.copy()
    project['uuid'] = str(uuid.uuid4())
    project['name'] = name
    project['priority'] = priority.upper()
    project['created'] = datetime.now().isoformat()
    project['record_modified'] = datetime.now().isoformat()
    project['tasks'] = {}
    return project


def new_task(note: str, priority: str = "MEDIUM") -> Dict:
    """Create new task dict from template"""
    task = TASK_TEMPLATE.copy()
    task['uuid'] = str(uuid.uuid4())
    task['note'] = note
    task['priority'] = priority.upper()
    task['created'] = datetime.now().isoformat()
    return task

# Basic validation
def validate_priority(priority: str) -> bool:
    """Check if priority is valid"""
    return priority.upper() in ['LOW', 'MEDIUM', 'HIGH']

# Validate data structure
def validate_data_structure(data: Dict) -> bool:
    """Validate loaded data has required structure"""
    required_keys = ['projects', 'stack']
    return all(key in data for key in required_keys)

# Remove non-alphanumeric except underscores, handle unicode
def sanitize_project_id(name: str) -> str:    
    return re.sub(r'[^\w]', '_', name.lower())