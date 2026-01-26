# Private Planner Examples

This directory contains example scripts demonstrating how to use Private Planner.

## Running the Examples

### Example Usage Script

```bash
python examples/example_usage.py
```

This example demonstrates:
- Creating a new experience plan
- Adding experiences with details (description, duration, tags)
- Getting AI-powered suggestions
- Exporting plans to JSON

## Creating Your Own Examples

You can create your own examples by importing the library:

```python
from privat_planner import ExperiencePlanner

planner = ExperiencePlanner()
plan = planner.create_plan("My Plan", ["activity1", "activity2"])
```

See `example_usage.py` for a complete working example.
