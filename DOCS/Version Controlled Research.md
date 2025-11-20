# Version Controlled Research - A Software Engineering Approach to Open Source, Decentralised Research

## Summed up simple version:
- Research project proposes a goal. "Analyse the Collatz Conjecture and its implications in binary representations."
- Researchers fork the project repository to their own accounts.
- Each researcher daisy-chains their work by creating branches for specific tasks, e.g., "data-collection", "theoretical-analysis", "simulation".
- Researchers commit changes with detailed messages, e.g., "Added data collection script for Collatz sequences up to 1 million."
- Once a task is complete, researchers create pull requests to merge their branches back into the main project repository.
- Peer review is conducted through comments on pull requests, ensuring quality and collaboration.

## Open Research Model: Fork and Merge
- Project Repository: Central repository hosting the research project.
- Forking: Researchers create their own copies of the project repository to work independently.
- Branching: Researchers create branches for specific tasks or experiments within their forked repositories.
- Committing: Researchers make changes and commit them with descriptive messages.
- Pull Requests: Researchers submit pull requests to propose merging their changes back into the main project repository.
- Peer Review: Other researchers review the pull requests, provide feedback, and suggest improvements.
- Merging: Once approved, changes are merged into the main project repository, updating the collective research.
- Continuous Integration: Automated tests and checks run on pull requests to ensure code quality and consistency.

### Structure:
- DOCS/: Documentation related to the research project.
- DATA/: Datasets used and generated during the research.
- SCRIPTS/: Code scripts for data analysis, simulations, and experiments.
- RESULTS/: Results and findings from the research.
- TESTS/: Automated tests for scripts and analyses.
- README.md: Overview of the research project, goals, and instructions for contributors.
- CONTRIBUTING.md: Guidelines for contributing to the research project.
- LICENSE: Licensing information for the research project.
- .gitignore: Specifies files and directories to be ignored by version control.

### Example Repository Structure:
```research-project/
├── DOCS/
│   ├── introduction.md
│   ├── methodology.md
│   └── references.md
├── DATA/
│   ├── raw/
│   └── processed/
├── SCRIPTS/
│   ├── data_collection.py
│   ├── analysis.py
│   └── simulation.py
├── RESULTS/
│   ├── figures/
│   └── tables/
├── TESTS/
│   ├── test_analysis.py
│   └── test_simulation.py
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── .gitignore
```
This structure and workflow facilitate collaborative, transparent, and reproducible research, leveraging the strengths of version control systems to manage contributions from multiple researchers effectively.
# Version Controlled Research - A Software Engineering Approach to Open Source, Decentralised Research
# Published as Public Domain 2024
# This work is dedicated to the public domain under the Creative Commons CC0 1.0 Universal (CC0 1.0) Public Domain Dedication. To view a copy of this dedication, visit https://creativecommons.org/publicdomain/zero/1.0/