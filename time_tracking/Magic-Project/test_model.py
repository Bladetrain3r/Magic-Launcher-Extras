#!/usr/bin/env python3
# test_model.py - Test script for MagicProjects data layer

import sys
from pathlib import Path

# Add components directory to path
sys.path.insert(0, str(Path(__file__).parent / 'components'))

from model import DataStore, new_project, new_task, sanitize_project_id

def test_basic_operations():
    """Test basic data store operations"""
    print("=== Testing MagicProjects Model ===\n")
    
    # Use test file instead of real one
    test_file = Path.home() / '.magicprojects' / 'test_projects.json'
    store = DataStore(test_file)
    
    print(f"1. Created datastore at: {test_file}")
    
    # Load initial data
    data = store.load()
    print(f"2. Loaded data: {len(data['projects'])} projects, {len(data['stack'])} in stack")
    
    # Create a test project
    project_id = sanitize_project_id("Test Project")
    data['projects'][project_id] = new_project("Test Project", "HIGH")
    print(f"3. Created project '{project_id}'")
    
    # Add a task
    task = new_task("Implement the thing", "MEDIUM")
    data['projects'][project_id]['tasks']['task_0'] = task
    print(f"4. Added task: {task['note'][:30]}...")
    
    # Add to stack
    data['stack'].insert(0, project_id)
    print(f"5. Added to stack")
    
    # Save
    store.save(data)
    print(f"6. Saved data")
    
    # Reload and verify
    data2 = store.load()
    assert project_id in data2['projects']
    assert project_id in data2['stack']
    assert 'task_0' in data2['projects'][project_id]['tasks']
    print(f"7. Verified data persisted correctly")
    
    # Test backup
    backup_file = store.backup('test')
    print(f"8. Created backup: {backup_file}")
    
    print("\n✓ All tests passed!")
    print(f"\nTest data location: {test_file}")
    print("Clean up with: rm ~/.magicprojects/test_projects.json*")

if __name__ == '__main__':
    try:
        test_basic_operations()
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)