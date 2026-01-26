"""
Data models for the Private Planner
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class Experience:
    """Represents a single experience in a plan"""
    
    name: str
    description: str = ""
    duration: Optional[int] = None  # in minutes
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert experience to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "duration": self.duration,
            "tags": self.tags,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Experience":
        """Create experience from dictionary"""
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            duration=data.get("duration"),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {})
        )


@dataclass
class Plan:
    """Represents an experience plan"""
    
    title: str
    experiences: List[Experience] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_experience(self, experience: Experience) -> None:
        """Add an experience to the plan"""
        self.experiences.append(experience)
        self.updated_at = datetime.now()
    
    def remove_experience(self, experience_name: str) -> bool:
        """Remove an experience from the plan by name"""
        original_length = len(self.experiences)
        self.experiences = [e for e in self.experiences if e.name != experience_name]
        if len(self.experiences) < original_length:
            self.updated_at = datetime.now()
            return True
        return False
    
    def get_total_duration(self) -> Optional[int]:
        """Calculate total duration of all experiences"""
        durations = [e.duration for e in self.experiences if e.duration is not None]
        if durations:
            return sum(durations)
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert plan to dictionary"""
        return {
            "title": self.title,
            "experiences": [e.to_dict() for e in self.experiences],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Plan":
        """Create plan from dictionary"""
        return cls(
            title=data["title"],
            experiences=[Experience.from_dict(e) for e in data.get("experiences", [])],
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
            metadata=data.get("metadata", {})
        )
