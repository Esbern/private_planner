# Private Planner

A semi AI/programmatic experience planner (the data lives elsewhere)

## Overview

Private Planner is a flexible experience planning tool that combines AI-assisted planning with programmatic control. It's designed to work with external data sources, making it perfect for personal planning, event management, and experience curation.

## Features

- **External Data Integration**: Connect to your data sources wherever they live
- **AI-Assisted Planning**: Semi-automated planning with intelligent suggestions
- **Programmatic API**: Full control through Python API
- **CLI Interface**: Command-line interface for quick operations
- **Flexible Architecture**: Extensible design for custom use cases

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from privat_planner import ExperiencePlanner

# Initialize planner with external data source
planner = ExperiencePlanner(data_source="path/to/data")

# Create a new experience plan
plan = planner.create_plan(
    title="Weekend Adventure",
    experiences=["hiking", "dining", "photography"]
)

# Get AI suggestions
suggestions = planner.get_suggestions(plan)

# Export the plan
planner.export_plan(plan, format="json")
```

## Command Line Usage

```bash
# Create a new plan
privat-planner create "Weekend Adventure" --experiences hiking,dining

# List existing plans
privat-planner list

# Get suggestions for a plan
privat-planner suggest "Weekend Adventure"
```

## Configuration

Create a `config.yaml` file to configure your data sources and preferences:

```yaml
data_source:
  type: "local"  # or "remote", "database", etc.
  path: "./data"
  
planner:
  ai_enabled: true
  suggestion_limit: 5
```

## License

Apache License 2.0