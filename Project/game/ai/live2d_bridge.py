"""Live2D emotion to motion mapping and parameter control."""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class EmotionMapping:
    """Maps an emotion to Live2D motions and parameters."""
    primary_motion: str
    fallback_motions: List[str]
    parameters: Dict[str, float]
    priority: int = 0


class Live2DBridge:
    """Manages emotion to Live2D motion/parameter mappings."""
    
    def __init__(self):
        """Initialize emotion mappings."""
        self.emotion_mappings = self._create_emotion_mappings()
        self.available_motions = [
            "idle", "happy", "excited", "shy", "nervous",
            "upset", "hmph", "disagreement", "neutral", "dancing"
        ]
        
        # Parameter names from Live2D model
        self.parameters = {
            "eye_smile": "ParamEyeLSmile",
            "eye_open_l": "ParamEyeLOpen",
            "eye_open_r": "ParamEyeROpen",
            "mouth_open": "ParamMouthOpenY",
            "brow_l": "ParamBrowLY",
            "brow_r": "ParamBrowRY",
            "body_angle_x": "ParamBodyAngleX",
            "body_angle_y": "ParamBodyAngleY",
            "body_angle_z": "ParamBodyAngleZ"
        }
    
    def _create_emotion_mappings(self) -> Dict[str, EmotionMapping]:
        """Create comprehensive emotion to motion mappings."""
        return {
            # Positive emotions
            "happy": EmotionMapping(
                primary_motion="happy",
                fallback_motions=["excited", "neutral"],
                parameters={"eye_smile": 0.8, "mouth_open": 0.3}
            ),
            "excited": EmotionMapping(
                primary_motion="excited",
                fallback_motions=["happy", "dancing"],
                parameters={"eye_smile": 0.6, "mouth_open": 0.5}
            ),
            "joyful": EmotionMapping(
                primary_motion="dancing",
                fallback_motions=["excited", "happy"],
                parameters={"eye_smile": 1.0, "mouth_open": 0.4}
            ),
            "content": EmotionMapping(
                primary_motion="neutral",
                fallback_motions=["idle", "happy"],
                parameters={"eye_smile": 0.3, "mouth_open": 0.1}
            ),
            
            # Shy/Embarrassed emotions
            "shy": EmotionMapping(
                primary_motion="shy",
                fallback_motions=["nervous", "neutral"],
                parameters={"eye_smile": 0.2, "brow_l": -0.3, "brow_r": -0.3}
            ),
            "embarrassed": EmotionMapping(
                primary_motion="shy",
                fallback_motions=["nervous", "upset"],
                parameters={"eye_smile": 0.1, "brow_l": -0.4, "brow_r": -0.4}
            ),
            "flustered": EmotionMapping(
                primary_motion="nervous",
                fallback_motions=["shy", "upset"],
                parameters={"eye_smile": 0.0, "brow_l": -0.5, "brow_r": -0.5}
            ),
            
            # Nervous/Anxious emotions
            "nervous": EmotionMapping(
                primary_motion="nervous",
                fallback_motions=["shy", "neutral"],
                parameters={"eye_open_l": 0.7, "eye_open_r": 0.7, "brow_l": -0.2}
            ),
            "anxious": EmotionMapping(
                primary_motion="nervous",
                fallback_motions=["upset", "neutral"],
                parameters={"eye_open_l": 0.8, "eye_open_r": 0.8, "brow_l": -0.3}
            ),
            "worried": EmotionMapping(
                primary_motion="upset",
                fallback_motions=["nervous", "neutral"],
                parameters={"brow_l": -0.4, "brow_r": -0.4, "mouth_open": 0.1}
            ),
            
            # Negative emotions
            "angry": EmotionMapping(
                primary_motion="hmph",
                fallback_motions=["disagreement", "upset"],
                parameters={"brow_l": -0.8, "brow_r": -0.8, "mouth_open": 0.0}
            ),
            "annoyed": EmotionMapping(
                primary_motion="hmph",
                fallback_motions=["disagreement", "neutral"],
                parameters={"brow_l": -0.6, "brow_r": -0.6, "mouth_open": 0.0}
            ),
            "frustrated": EmotionMapping(
                primary_motion="disagreement",
                fallback_motions=["hmph", "upset"],
                parameters={"brow_l": -0.7, "brow_r": -0.7, "mouth_open": 0.2}
            ),
            "upset": EmotionMapping(
                primary_motion="upset",
                fallback_motions=["disagreement", "nervous"],
                parameters={"brow_l": -0.5, "brow_r": -0.5, "eye_smile": -0.3}
            ),
            "sad": EmotionMapping(
                primary_motion="upset",
                fallback_motions=["nervous", "neutral"],
                parameters={"brow_l": -0.3, "brow_r": -0.3, "eye_smile": -0.5}
            ),
            
            # Neutral/Contemplative emotions
            "neutral": EmotionMapping(
                primary_motion="neutral",
                fallback_motions=["idle"],
                parameters={}
            ),
            "thinking": EmotionMapping(
                primary_motion="neutral",
                fallback_motions=["idle"],
                parameters={"brow_l": 0.2, "eye_open_l": 0.9}
            ),
            "curious": EmotionMapping(
                primary_motion="neutral",
                fallback_motions=["idle", "happy"],
                parameters={"brow_l": 0.3, "brow_r": 0.3, "eye_open_l": 1.0}
            ),
            "confused": EmotionMapping(
                primary_motion="disagreement",
                fallback_motions=["neutral", "nervous"],
                parameters={"brow_l": 0.1, "brow_r": -0.1}
            ),
            
            # Special/Complex emotions
            "determined": EmotionMapping(
                primary_motion="neutral",
                fallback_motions=["idle"],
                parameters={"brow_l": -0.2, "brow_r": -0.2, "mouth_open": 0.0}
            ),
            "surprised": EmotionMapping(
                primary_motion="excited",
                fallback_motions=["happy", "neutral"],
                parameters={"eye_open_l": 1.0, "eye_open_r": 1.0, "mouth_open": 0.6}
            ),
            "playful": EmotionMapping(
                primary_motion="dancing",
                fallback_motions=["happy", "excited"],
                parameters={"eye_smile": 0.7, "mouth_open": 0.3}
            ),
            "sarcastic": EmotionMapping(
                primary_motion="hmph",
                fallback_motions=["disagreement", "neutral"],
                parameters={"eye_smile": 0.2, "brow_l": 0.1, "brow_r": -0.1}
            ),
            
            # Default/Idle state
            "idle": EmotionMapping(
                primary_motion="idle",
                fallback_motions=["neutral"],
                parameters={}
            )
        }
    
    def get_motion_for_emotion(self, emotion: str) -> str:
        """Get the best motion for an emotion.
        
        Args:
            emotion: The emotion name
            
        Returns:
            Motion file name (without extension)
        """
        emotion = emotion.lower().strip()
        
        # Direct mapping exists
        if emotion in self.emotion_mappings:
            mapping = self.emotion_mappings[emotion]
            
            # Try primary motion first
            if mapping.primary_motion in self.available_motions:
                logger.debug(f"Using primary motion '{mapping.primary_motion}' for emotion '{emotion}'")
                return mapping.primary_motion
            
            # Try fallback motions
            for fallback in mapping.fallback_motions:
                if fallback in self.available_motions:
                    logger.debug(f"Using fallback motion '{fallback}' for emotion '{emotion}'")
                    return fallback
        
        # No direct mapping, try to find similar emotion
        similar = self._find_similar_emotion(emotion)
        if similar:
            logger.debug(f"Using similar emotion '{similar}' for '{emotion}'")
            return self.get_motion_for_emotion(similar)
        
        # Default to idle
        logger.warning(f"No motion mapping for emotion '{emotion}', using idle")
        return "idle"
    
    def get_parameters_for_emotion(self, emotion: str) -> Dict[str, float]:
        """Get Live2D parameters for an emotion.
        
        Args:
            emotion: The emotion name
            
        Returns:
            Dictionary of parameter_id -> value
        """
        emotion = emotion.lower().strip()
        
        if emotion in self.emotion_mappings:
            mapping = self.emotion_mappings[emotion]
            
            # Convert friendly names to actual parameter IDs
            result = {}
            for param_name, value in mapping.parameters.items():
                if param_name in self.parameters:
                    result[self.parameters[param_name]] = value
                else:
                    logger.warning(f"Unknown parameter name: {param_name}")
            
            return result
        
        # Try similar emotion
        similar = self._find_similar_emotion(emotion)
        if similar:
            return self.get_parameters_for_emotion(similar)
        
        # Return empty for default state
        return {}
    
    def _find_similar_emotion(self, emotion: str) -> Optional[str]:
        """Find a similar emotion based on keywords."""
        emotion_lower = emotion.lower()
        
        # Keyword mappings to base emotions
        keyword_map = {
            "smile": "happy",
            "laugh": "happy",
            "joy": "joyful",
            "excite": "excited",
            "enthus": "excited",
            "bash": "shy",
            "blush": "shy",
            "timid": "shy",
            "worry": "worried",
            "concern": "worried",
            "fear": "nervous",
            "anger": "angry",
            "mad": "angry",
            "rage": "angry",
            "irritat": "annoyed",
            "disappoint": "upset",
            "sorrow": "sad",
            "depress": "sad",
            "think": "thinking",
            "ponder": "thinking",
            "wonder": "curious",
            "puzzle": "confused",
            "bewilder": "confused"
        }
        
        for keyword, mapped_emotion in keyword_map.items():
            if keyword in emotion_lower:
                return mapped_emotion
        
        return None
    
    def get_emotion_list(self) -> List[str]:
        """Get list of all supported emotions."""
        return list(self.emotion_mappings.keys())
    
    def get_motion_list(self) -> List[str]:
        """Get list of all available motions."""
        return self.available_motions.copy()
    
    def validate_motion(self, motion: str) -> bool:
        """Check if a motion exists."""
        return motion in self.available_motions
    
    def get_emotion_info(self, emotion: str) -> Optional[EmotionMapping]:
        """Get full emotion mapping information."""
        return self.emotion_mappings.get(emotion.lower().strip())


# Global bridge instance
_bridge: Optional[Live2DBridge] = None


def get_live2d_bridge() -> Live2DBridge:
    """Get or create the global Live2D bridge instance."""
    global _bridge
    if _bridge is None:
        _bridge = Live2DBridge()
    return _bridge


# Convenience functions
def get_motion_for_emotion(emotion: str) -> str:
    """Get the best motion for an emotion."""
    return get_live2d_bridge().get_motion_for_emotion(emotion)


def get_parameters_for_emotion(emotion: str) -> Dict[str, float]:
    """Get Live2D parameters for an emotion."""
    return get_live2d_bridge().get_parameters_for_emotion(emotion)


def get_supported_emotions() -> List[str]:
    """Get list of all supported emotions."""
    return get_live2d_bridge().get_emotion_list()