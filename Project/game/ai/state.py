"""Save-compatible state management for dynamic CYOA."""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime


logger = logging.getLogger(__name__)


@dataclass
class Choice:
    """Represents a player choice."""
    scene_id: str
    choice_text: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Choice':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class SceneSummary:
    """Summary of a completed scene."""
    scene_id: str
    summary: str
    choices_presented: List[str]
    choice_made: Optional[str]
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SceneSummary':
        """Create from dictionary."""
        return cls(**data)


class GameState:
    """Manages game state for save/load compatibility."""
    
    def __init__(self):
        """Initialize empty game state."""
        self.player_choices: List[Choice] = []
        self.world_facts: Dict[str, Any] = {}
        self.scene_summaries: List[SceneSummary] = []
        self.current_scene_id: Optional[str] = None
        self.metadata: Dict[str, Any] = {
            'version': '1.0.0',
            'created': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        # Runtime state (not saved)
        self._cache: Dict[str, Any] = {}
        self._listeners: List[callable] = []
    
    def add_choice(self, scene_id: str, choice_text: str, 
                  metadata: Optional[Dict[str, Any]] = None):
        """Add a player choice to history."""
        choice = Choice(
            scene_id=scene_id,
            choice_text=choice_text,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {}
        )
        self.player_choices.append(choice)
        self._notify_listeners('choice_added', choice)
        logger.debug(f"Added choice: {choice_text} in scene {scene_id}")
    
    def set_world_fact(self, key: str, value: Any):
        """Set a world fact."""
        old_value = self.world_facts.get(key)
        self.world_facts[key] = value
        self._notify_listeners('fact_changed', {'key': key, 'old': old_value, 'new': value})
        logger.debug(f"Set world fact: {key} = {value}")
    
    def get_world_fact(self, key: str, default: Any = None) -> Any:
        """Get a world fact."""
        return self.world_facts.get(key, default)
    
    def add_scene_summary(self, scene_id: str, summary: str,
                         choices_presented: List[str],
                         choice_made: Optional[str] = None,
                         metadata: Optional[Dict[str, Any]] = None):
        """Add a scene summary."""
        scene_summary = SceneSummary(
            scene_id=scene_id,
            summary=summary,
            choices_presented=choices_presented,
            choice_made=choice_made,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {}
        )
        self.scene_summaries.append(scene_summary)
        self._notify_listeners('scene_completed', scene_summary)
        logger.debug(f"Added scene summary for: {scene_id}")
    
    def get_recent_summaries(self, count: int = 5) -> List[SceneSummary]:
        """Get recent scene summaries."""
        return self.scene_summaries[-count:] if self.scene_summaries else []
    
    def get_recent_choices(self, count: int = 10) -> List[Choice]:
        """Get recent player choices."""
        return self.player_choices[-count:] if self.player_choices else []
    
    def to_dict(self) -> dict:
        """Convert state to dictionary for Ren'Py save system."""
        self.metadata['last_updated'] = datetime.now().isoformat()
        
        return {
            'player_choices': [c.to_dict() for c in self.player_choices],
            'world_facts': self.world_facts,
            'scene_summaries': [s.to_dict() for s in self.scene_summaries],
            'current_scene_id': self.current_scene_id,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GameState':
        """Create state from dictionary (for loading saves)."""
        state = cls()
        
        # Restore choices
        state.player_choices = [
            Choice.from_dict(c) for c in data.get('player_choices', [])
        ]
        
        # Restore world facts
        state.world_facts = data.get('world_facts', {})
        
        # Restore scene summaries
        state.scene_summaries = [
            SceneSummary.from_dict(s) for s in data.get('scene_summaries', [])
        ]
        
        # Restore other fields
        state.current_scene_id = data.get('current_scene_id')
        state.metadata = data.get('metadata', state.metadata)
        
        logger.info(f"Loaded game state with {len(state.player_choices)} choices, "
                   f"{len(state.world_facts)} facts, {len(state.scene_summaries)} scenes")
        
        return state
    
    def update(self, other: 'GameState'):
        """Update this state with data from another state."""
        self.player_choices = other.player_choices.copy()
        self.world_facts = other.world_facts.copy()
        self.scene_summaries = other.scene_summaries.copy()
        self.current_scene_id = other.current_scene_id
        self.metadata = other.metadata.copy()
        self._notify_listeners('state_updated', self)
    
    def clear(self):
        """Clear all state data."""
        self.player_choices.clear()
        self.world_facts.clear()
        self.scene_summaries.clear()
        self.current_scene_id = None
        self.metadata = {
            'version': '1.0.0',
            'created': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        self._cache.clear()
        self._notify_listeners('state_cleared', None)
        logger.info("Cleared game state")
    
    def get_context_for_ai(self, include_summaries: int = 3,
                          include_choices: int = 5) -> str:
        """Get formatted context string for AI agents."""
        context_parts = []
        
        # Add recent scene summaries
        recent_summaries = self.get_recent_summaries(include_summaries)
        if recent_summaries:
            context_parts.append("=== Recent Scene History ===")
            for summary in recent_summaries:
                context_parts.append(f"Scene {summary.scene_id}: {summary.summary}")
                if summary.choice_made:
                    context_parts.append(f"  Player chose: {summary.choice_made}")
        
        # Add recent choices
        recent_choices = self.get_recent_choices(include_choices)
        if recent_choices:
            context_parts.append("\n=== Recent Player Choices ===")
            for choice in recent_choices:
                context_parts.append(f"- {choice.choice_text} (in {choice.scene_id})")
        
        # Add important world facts
        if self.world_facts:
            context_parts.append("\n=== World Facts ===")
            for key, value in self.world_facts.items():
                if not key.startswith('_'):  # Skip private facts
                    context_parts.append(f"- {key}: {value}")
        
        return "\n".join(context_parts)
    
    def add_listener(self, callback: callable):
        """Add a state change listener."""
        self._listeners.append(callback)
    
    def remove_listener(self, callback: callable):
        """Remove a state change listener."""
        if callback in self._listeners:
            self._listeners.remove(callback)
    
    def _notify_listeners(self, event_type: str, data: Any):
        """Notify all listeners of state change."""
        for listener in self._listeners:
            try:
                listener(event_type, data)
            except Exception as e:
                logger.error(f"Error notifying listener: {e}")
    
    def __repr__(self) -> str:
        """String representation."""
        return (f"GameState(choices={len(self.player_choices)}, "
               f"facts={len(self.world_facts)}, "
               f"summaries={len(self.scene_summaries)})")


# Global state instance
_game_state: Optional[GameState] = None


def get_game_state() -> GameState:
    """Get or create the global game state instance."""
    global _game_state
    if _game_state is None:
        _game_state = GameState()
    return _game_state


def set_game_state(state: GameState):
    """Set the global game state instance."""
    global _game_state
    _game_state = state


def reset_game_state():
    """Reset the global game state."""
    global _game_state
    if _game_state:
        _game_state.clear()
    else:
        _game_state = GameState()