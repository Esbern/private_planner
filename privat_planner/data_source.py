"""
Data source management for external data integration
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml


class DataSource:
    """Base class for data sources"""
    
    def load_data(self) -> Dict[str, Any]:
        """Load data from the source"""
        raise NotImplementedError
    
    def save_data(self, data: Dict[str, Any]) -> None:
        """Save data to the source"""
        raise NotImplementedError


class LocalDataSource(DataSource):
    """Local file-based data source"""
    
    def __init__(self, path: str):
        """Initialize local data source
        
        Args:
            path: Path to the data directory or file
        """
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
    
    def load_data(self) -> Dict[str, Any]:
        """Load data from local files"""
        data = {"plans": [], "experiences": []}
        
        plans_file = self.path / "plans.json"
        if plans_file.exists():
            with open(plans_file, "r") as f:
                data["plans"] = json.load(f)
        
        experiences_file = self.path / "experiences.json"
        if experiences_file.exists():
            with open(experiences_file, "r") as f:
                data["experiences"] = json.load(f)
        
        return data
    
    def save_data(self, data: Dict[str, Any]) -> None:
        """Save data to local files"""
        if "plans" in data:
            plans_file = self.path / "plans.json"
            with open(plans_file, "w") as f:
                json.dump(data["plans"], f, indent=2)
        
        if "experiences" in data:
            experiences_file = self.path / "experiences.json"
            with open(experiences_file, "w") as f:
                json.dump(data["experiences"], f, indent=2)
    
    def save_plan(self, plan_dict: Dict[str, Any]) -> None:
        """Save a single plan"""
        data = self.load_data()
        plans = data.get("plans", [])
        
        # Update existing or add new
        existing_index = None
        for i, p in enumerate(plans):
            if p.get("title") == plan_dict.get("title"):
                existing_index = i
                break
        
        if existing_index is not None:
            plans[existing_index] = plan_dict
        else:
            plans.append(plan_dict)
        
        data["plans"] = plans
        self.save_data(data)
    
    def get_plan(self, title: str) -> Optional[Dict[str, Any]]:
        """Get a plan by title"""
        data = self.load_data()
        for plan in data.get("plans", []):
            if plan.get("title") == title:
                return plan
        return None
    
    def list_plans(self) -> List[Dict[str, Any]]:
        """List all plans"""
        data = self.load_data()
        return data.get("plans", [])


class ConfigLoader:
    """Configuration loader for the planner"""
    
    @staticmethod
    def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file
        
        Args:
            config_path: Path to config file (defaults to config.yaml in current dir)
        
        Returns:
            Configuration dictionary
        """
        if config_path is None:
            config_path = "config.yaml"
        
        config_file = Path(config_path)
        if not config_file.exists():
            return ConfigLoader.get_default_config()
        
        with open(config_file, "r") as f:
            return yaml.safe_load(f) or ConfigLoader.get_default_config()
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "data_source": {
                "type": "local",
                "path": "./data"
            },
            "planner": {
                "ai_enabled": True,
                "suggestion_limit": 5
            }
        }
