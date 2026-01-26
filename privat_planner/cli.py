"""
Command-line interface for Private Planner
"""

import sys
import argparse
from typing import List, Optional
from privat_planner import ExperiencePlanner
from privat_planner.models import Experience


def create_plan_command(args):
    """Handle create plan command"""
    planner = ExperiencePlanner()
    
    experiences = []
    if args.experiences:
        experiences = [exp.strip() for exp in args.experiences.split(",")]
    
    plan = planner.create_plan(args.title, experiences)
    
    print(f"Created plan: {plan.title}")
    if plan.experiences:
        print(f"  Experiences: {', '.join([e.name for e in plan.experiences])}")
    
    return 0


def list_plans_command(args):
    """Handle list plans command"""
    planner = ExperiencePlanner()
    plans = planner.list_plans()
    
    if not plans:
        print("No plans found.")
        return 0
    
    print(f"Found {len(plans)} plan(s):")
    for plan in plans:
        print(f"\n  • {plan.title}")
        print(f"    Created: {plan.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"    Experiences: {len(plan.experiences)}")
        if plan.experiences:
            exp_names = [e.name for e in plan.experiences]
            print(f"    - {', '.join(exp_names)}")
    
    return 0


def show_plan_command(args):
    """Handle show plan command"""
    planner = ExperiencePlanner()
    plan = planner.get_plan(args.title)
    
    if not plan:
        print(f"Plan not found: {args.title}")
        return 1
    
    print(f"Plan: {plan.title}")
    print(f"Created: {plan.created_at.strftime('%Y-%m-%d %H:%M')}")
    print(f"Updated: {plan.updated_at.strftime('%Y-%m-%d %H:%M')}")
    
    if plan.experiences:
        print(f"\nExperiences ({len(plan.experiences)}):")
        for i, exp in enumerate(plan.experiences, 1):
            print(f"\n  {i}. {exp.name}")
            if exp.description:
                print(f"     Description: {exp.description}")
            if exp.duration:
                print(f"     Duration: {exp.duration} minutes")
            if exp.tags:
                print(f"     Tags: {', '.join(exp.tags)}")
    
    total_duration = plan.get_total_duration()
    if total_duration:
        hours = total_duration // 60
        minutes = total_duration % 60
        print(f"\nTotal Duration: {hours}h {minutes}m")
    
    return 0


def suggest_command(args):
    """Handle suggest command"""
    planner = ExperiencePlanner()
    plan = planner.get_plan(args.title)
    
    if not plan:
        print(f"Plan not found: {args.title}")
        return 1
    
    suggestions = planner.get_suggestions(plan)
    
    if not suggestions:
        print("No suggestions available.")
        return 0
    
    print(f"Suggestions for '{plan.title}':\n")
    for i, suggestion in enumerate(suggestions, 1):
        priority = suggestion.get("priority", "medium").upper()
        message = suggestion.get("message", "")
        print(f"  {i}. [{priority}] {message}")
    
    return 0


def export_command(args):
    """Handle export command"""
    planner = ExperiencePlanner()
    plan = planner.get_plan(args.title)
    
    if not plan:
        print(f"Plan not found: {args.title}")
        return 1
    
    output_path = args.output or f"{plan.title.replace(' ', '_').lower()}.{args.format}"
    exported = planner.export_plan(plan, format=args.format, output_path=output_path)
    
    print(f"Exported plan to: {output_path}")
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Private Planner - A semi AI/programmatic experience planner"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new plan")
    create_parser.add_argument("title", help="Title of the plan")
    create_parser.add_argument(
        "--experiences",
        help="Comma-separated list of experiences"
    )
    create_parser.set_defaults(func=create_plan_command)
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all plans")
    list_parser.set_defaults(func=list_plans_command)
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show plan details")
    show_parser.add_argument("title", help="Title of the plan")
    show_parser.set_defaults(func=show_plan_command)
    
    # Suggest command
    suggest_parser = subparsers.add_parser("suggest", help="Get AI suggestions for a plan")
    suggest_parser.add_argument("title", help="Title of the plan")
    suggest_parser.set_defaults(func=suggest_command)
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export a plan")
    export_parser.add_argument("title", help="Title of the plan")
    export_parser.add_argument(
        "--format",
        choices=["json", "yaml"],
        default="json",
        help="Export format"
    )
    export_parser.add_argument(
        "--output",
        help="Output file path"
    )
    export_parser.set_defaults(func=export_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
