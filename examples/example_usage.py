#!/usr/bin/env python3
"""
Example usage of Private Planner
"""

from privat_planner import ExperiencePlanner
from privat_planner.models import Experience

def main():
    # Initialize the planner
    planner = ExperiencePlanner()
    
    # Create a new plan
    plan = planner.create_plan(
        title="Weekend Getaway",
        experiences=["hiking", "camping", "photography"]
    )
    
    print(f"Created plan: {plan.title}")
    
    # Add more details to experiences
    for exp in plan.experiences:
        if exp.name == "hiking":
            exp.description = "Mountain trail hike"
            exp.duration = 180  # 3 hours
            exp.tags = ["outdoor", "active", "nature"]
        elif exp.name == "camping":
            exp.description = "Overnight camping"
            exp.duration = 720  # 12 hours
            exp.tags = ["outdoor", "relaxing"]
        elif exp.name == "photography":
            exp.description = "Landscape photography"
            exp.duration = 120  # 2 hours
            exp.tags = ["outdoor", "creative"]
    
    # Update the plan
    planner.update_plan(plan)
    
    # Get suggestions
    suggestions = planner.get_suggestions(plan)
    print(f"\nAI Suggestions ({len(suggestions)}):")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. [{suggestion['priority']}] {suggestion['message']}")
    
    # Show plan details
    print(f"\nPlan Details:")
    print(f"  Title: {plan.title}")
    print(f"  Total Duration: {plan.get_total_duration()} minutes")
    print(f"  Experiences:")
    for exp in plan.experiences:
        print(f"    - {exp.name}: {exp.duration}min, tags: {', '.join(exp.tags)}")
    
    # Export the plan
    exported_json = planner.export_plan(plan, format="json")
    print(f"\nExported to JSON (first 200 chars):")
    print(exported_json[:200] + "...")

if __name__ == "__main__":
    main()
