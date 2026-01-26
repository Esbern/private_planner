"""
Main planner implementation with AI-assisted planning capabilities
"""

from typing import List, Dict, Any, Optional
from privat_planner.models import Plan, Experience
from privat_planner.data_source import DataSource, LocalDataSource, ConfigLoader


class ExperiencePlanner:
    """Main experience planner class that combines AI and programmatic planning"""
    
    def __init__(self, data_source: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """Initialize the experience planner
        
        Args:
            data_source: Path to data source (optional, uses config if not provided)
            config: Configuration dictionary (optional, loads from file if not provided)
        """
        if config is None:
            config = ConfigLoader.load_config()
        
        self.config = config
        self.ai_enabled = config.get("planner", {}).get("ai_enabled", True)
        self.suggestion_limit = config.get("planner", {}).get("suggestion_limit", 5)
        
        # Initialize data source
        if data_source is None:
            data_source = config.get("data_source", {}).get("path", "./data")
        
        source_type = config.get("data_source", {}).get("type", "local")
        if source_type == "local":
            self.data_source = LocalDataSource(data_source)
        else:
            # Fallback to local
            self.data_source = LocalDataSource(data_source)
    
    def create_plan(self, title: str, experiences: Optional[List[str]] = None) -> Plan:
        """Create a new experience plan
        
        Args:
            title: Title of the plan
            experiences: List of experience names to include
        
        Returns:
            New Plan object
        """
        plan = Plan(title=title)
        
        if experiences:
            for exp_name in experiences:
                experience = Experience(name=exp_name)
                plan.add_experience(experience)
        
        # Save the plan
        self.data_source.save_plan(plan.to_dict())
        
        return plan
    
    def get_plan(self, title: str) -> Optional[Plan]:
        """Get an existing plan by title
        
        Args:
            title: Title of the plan to retrieve
        
        Returns:
            Plan object or None if not found
        """
        plan_dict = self.data_source.get_plan(title)
        if plan_dict:
            return Plan.from_dict(plan_dict)
        return None
    
    def list_plans(self) -> List[Plan]:
        """List all plans
        
        Returns:
            List of Plan objects
        """
        plans_data = self.data_source.list_plans()
        return [Plan.from_dict(p) for p in plans_data]
    
    def update_plan(self, plan: Plan) -> None:
        """Update an existing plan
        
        Args:
            plan: Plan object to update
        """
        self.data_source.save_plan(plan.to_dict())
    
    def get_suggestions(self, plan: Plan) -> List[Dict[str, Any]]:
        """Get AI-powered suggestions for a plan
        
        This is a semi-AI feature that provides intelligent suggestions
        based on the plan's current experiences.
        
        Args:
            plan: Plan to get suggestions for
        
        Returns:
            List of suggestion dictionaries
        """
        if not self.ai_enabled:
            return []
        
        suggestions = []
        
        # Extract tags from existing experiences
        all_tags = set()
        for exp in plan.experiences:
            all_tags.update(exp.tags)
        
        # Generate suggestions based on existing experiences
        # This is a simplified version - in a real implementation,
        # this would use actual AI/ML models
        suggestion_templates = [
            {
                "type": "duration",
                "message": "Consider adding duration estimates to your experiences",
                "priority": "high"
            },
            {
                "type": "tags",
                "message": "Add tags to categorize your experiences better",
                "priority": "medium"
            },
            {
                "type": "balance",
                "message": "Your plan looks well-balanced",
                "priority": "low"
            }
        ]
        
        # Filter suggestions based on plan state
        for template in suggestion_templates[:self.suggestion_limit]:
            if template["type"] == "duration":
                missing_duration = any(e.duration is None for e in plan.experiences)
                if missing_duration:
                    suggestions.append(template)
            elif template["type"] == "tags":
                missing_tags = any(len(e.tags) == 0 for e in plan.experiences)
                if missing_tags:
                    suggestions.append(template)
            else:
                suggestions.append(template)
        
        return suggestions
    
    def export_plan(self, plan: Plan, format: str = "json", output_path: Optional[str] = None) -> str:
        """Export a plan to a file
        
        Args:
            plan: Plan to export
            format: Export format (json, yaml)
            output_path: Optional output file path
        
        Returns:
            Exported data as string
        """
        import json
        
        if format == "json":
            exported = json.dumps(plan.to_dict(), indent=2)
        elif format == "yaml":
            import yaml
            exported = yaml.dump(plan.to_dict(), default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        if output_path:
            with open(output_path, "w") as f:
                f.write(exported)
        
        return exported
