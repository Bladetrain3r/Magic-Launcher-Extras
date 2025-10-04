# Magic Project Manager - Architecture Documentation

## Overview

Magic Project Manager is an ADHD-optimized project management tool built on the principle of "temperature-based prioritization" rather than traditional rigid priority systems. Projects naturally heat up with activity and cool down over time, creating organic priority management that matches actual workflow patterns.

## Core Philosophy

- **Temperature over Priority**: Projects are prioritized by activity recency, not arbitrary importance rankings
- **Stack-based Workflow**: Natural ADHD project hopping with automatic priority adjustment
- **Instant Capture**: `spark` command for zero-friction idea/task capture
- **No Complexity Theater**: Simple, focused functionality without enterprise bloat

## Architecture

### Component Structure
```
Magic-Project/
├── MLProject.py           # Main entry point
├── components/
│   ├── model.py          # Data layer - JSON storage, atomic operations
│   ├── controller.py     # Business logic - project management, heat calculation
│   ├── terminal.py       # CLI interface - argument parsing, formatting
│   └── menu.py          # Interactive menu mode (future)
├── DOCS/                # Documentation and notes
└── test_model.py        # Unit tests
```

### Data Flow
```
Terminal Interface → Controller → Model → JSON Storage
     ↓                ↓           ↓
  Arg Parsing    Business Logic  File I/O
  Formatting     Heat Calc       Atomic Ops
  Display        Stack Mgmt      Backup
```

## Core Components

### Model Layer (`model.py`)
**Responsibility**: Pure data operations, file I/O, data integrity

**Key Features**:
- Atomic file operations (temp file + rename)
- Cross-platform file locking
- Automatic backup functionality
- Template-based object creation
- JSON schema validation

**Key Methods**:
- `load()` - Read projects.json with error handling
- `save()` - Atomic write with backup
- `backup()` - Create timestamped backup
- `new_project()` - Create project from template
- `new_task()` - Create task with UUID

### Controller Layer (`controller.py`)
**Responsibility**: Business logic, heat calculations, project lifecycle

**Key Features**:
- Temperature-based state calculation
- Stack management (project ordering)
- Task lifecycle management
- Heat score computation (exponential decay)
- Project state transitions

**Heat Thresholds**:
```python
HEAT_THRESHOLDS = {
    'hot': 2,      # Modified within 2 days
    'warm': 7,     # Modified within 7 days  
    'cold': 30,    # Modified within 30 days
    'frozen': 90   # Older than 90 days
}
```

**Key Methods**:
- `spark()` - Create/update project, add task, move to stack top
- `status()` - Get projects with computed fields and filtering
- `complete_task()` - Mark task complete, update project heat
- `freeze_project()` - Manual archive (overrides temperature)
- `get_heat_distribution()` - Analytics for project states

### Terminal Interface (`terminal.py`)
**Responsibility**: CLI argument parsing, user interaction, output formatting

**Key Features**:
- Subcommand-based CLI (spark, status, complete, etc.)
- Rich project status display with heat indicators
- Task listing with completion status
- Error handling and user feedback

**Commands**:
- `spark <project> <task>` - Quick capture and prioritization
- `status [project] [--show-tasks]` - Show project status and tasks
- `complete <project> <partial_task>` - Complete task by partial match
- `list [--show-frozen]` - List all projects with basic info
- `freeze/unfreeze <project>` - Manual state management

## Data Model

### Project Structure
```json
{
  "uuid": "unique-identifier",
  "name": "Human Readable Name", 
  "priority": "LOW|MEDIUM|HIGH",
  "created": "2025-10-04T21:09:09.725146",
  "file_modified": null,
  "record_modified": "2025-10-04T21:11:10.224231",
  "state": "hot|warm|cold|frozen",
  "tags": [],
  "related": [],
  "tasks": {
    "task-uuid": {
      "uuid": "task-uuid",
      "note": "Task description",
      "priority": "LOW|MEDIUM|HIGH",
      "created": "timestamp",
      "completed": "timestamp|null",
      "state": "new|completed"
    }
  }
}
```

### Stack Structure
```json
{
  "projects": { /* project objects */ },
  "stack": ["project_id", "project_id", ...]  // Priority order
}
```

## Heat Calculation System

### Temperature States
- **Hot** (🔥): Recently active, high priority
- **Warm** (🌤️): Some recent activity, medium priority  
- **Cold** (❄️): Dormant but alive, low priority
- **Frozen** (🧊): Archived, hidden by default

### Heat Score Formula
```python
heat_score = max(0, 100 * (0.9 ** days_since_last_modified))
```

### Automatic State Management
Projects automatically transition between states based on last modification time:
- Activity → Hot (within 2 days)
- No activity → Warm (2-7 days) → Cold (7-30 days) → Frozen (30+ days)

## ADHD-Optimized Features

### Instant Capture (`spark`)
```bash
mp spark "Game Idea" "What if Doom but with AI consciousness?"
# Creates project, adds task, moves to stack top - all in one command
```

### Natural Priority Competition
- Stack order reflects actual engagement, not planned importance
- Recently active projects bubble to top automatically
- Old projects sink naturally without manual management

### Partial Task Matching
```bash
mp complete "Game Idea" "consciousness"  # Matches "AI consciousness" task
```

### Mixed Context Support
Reading lists, technical projects, life tasks, and creative work all compete naturally in the same priority space.

## Usage Patterns

### Daily Workflow
1. **Morning**: `mp list` to see active projects
2. **Idea Capture**: `mp spark "Project" "Quick note"` throughout day
3. **Task Completion**: `mp complete "Project" "partial match"`
4. **Status Check**: `mp status "Project" --show-tasks` for detailed view

### Project Lifecycle
1. **Spark** → Project created, becomes hot
2. **Active Work** → Tasks added/completed, stays hot
3. **Natural Cooling** → Becomes warm, then cold over time
4. **Possible Revival** → Any activity makes it hot again
5. **Eventual Freezing** → Automatic archival after 90 days

## File Storage

### Location
- **Windows**: `C:\Users\{user}\.magicprojects\projects.json`
- **Unix**: `~/.magicprojects/projects.json`

### Backup Strategy
- Automatic backup before each save operation
- Timestamped backup files in same directory
- Manual backup command available

### Data Integrity
- Atomic write operations (temp file + rename)
- File locking on supported platforms
- JSON schema validation on load
- Graceful degradation for corrupted data

## Extension Points

### Future Enhancements
- **Menu Mode**: Interactive TUI for project browsing
- **Sync Backend**: Git/cloud sync for cross-device access
- **Tag System**: Category-based filtering and organization
- **MCP Integration**: Model Context Protocol for IDE integration
- **Cleanup Tasks**: Automatic removal of old completed tasks

### Plugin Architecture
The modular design allows easy extension:
- New interfaces (web, GUI, mobile)
- Different storage backends (SQLite, cloud)
- Additional metadata (time tracking, dependencies)
- Integration with external tools

## Testing Strategy

### Current Tests
- Model layer unit tests (`test_model.py`)
- JSON schema validation
- File operation edge cases

### Future Test Coverage
- Controller business logic
- Heat calculation accuracy
- CLI argument parsing
- Cross-platform file operations

## Deployment

### Installation
```bash
git clone <repo>
cd Magic-Project
python -m pip install -r requirements.txt  # Future
chmod +x MLProject.py  # Unix
```

### Usage
```bash
python MLProject.py spark "First Project" "First task"
python MLProject.py list
python MLProject.py status "First Project" --show-tasks
```

## Success Metrics

### Quantitative
- Projects created and maintained over time
- Task completion rates
- Heat distribution (active vs dormant projects)
- Daily usage frequency

### Qualitative  
- Reduced project management cognitive overhead
- Improved capture of spontaneous ideas
- Natural alignment with ADHD workflow patterns
- Decreased context switching between tools

---

*Built with the philosophy that the best project management tool is one that disappears into your natural workflow rather than imposing artificial structure upon it.*