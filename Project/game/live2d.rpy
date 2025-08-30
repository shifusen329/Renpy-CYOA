# Live2D Character Integration

init python:
    import os
    import sys
    
    # Add AI module to path if needed
    if "game/ai" not in sys.path:
        sys.path.append(os.path.join(config.gamedir, "ai"))
    
    # Import Live2D bridge
    try:
        from live2d_bridge import (
            get_motion_for_emotion,
            get_parameters_for_emotion,
            get_supported_emotions,
            get_live2d_bridge
        )
        live2d_bridge_loaded = True
    except ImportError as e:
        live2d_bridge_loaded = False
        print(f"Warning: Could not load Live2D bridge: {e}")
        # Fallback functions
        def get_motion_for_emotion(emotion):
            return "idle"
        def get_parameters_for_emotion(emotion):
            return {}
        def get_supported_emotions():
            return ["neutral"]
    
    # Live2D motion path helper
    def get_motion_path(motion_name):
        """Get full path to motion file."""
        if not motion_name.endswith('.motion3.json'):
            motion_name = f"{motion_name}.motion3.json"
        return f"../Ivy/motion/{motion_name}"
    
    # Character emotion state tracker
    class CharacterEmotionState:
        def __init__(self):
            self.current_emotion = "neutral"
            self.current_motion = "idle"
            self.emotion_history = []
            
        def set_emotion(self, emotion):
            """Set character emotion and update motion."""
            if emotion != self.current_emotion:
                self.emotion_history.append(self.current_emotion)
                if len(self.emotion_history) > 10:
                    self.emotion_history.pop(0)
                
                self.current_emotion = emotion
                self.current_motion = get_motion_for_emotion(emotion)
                return self.current_motion
            return None
        
        def get_current_motion_path(self):
            """Get path to current motion file."""
            return get_motion_path(self.current_motion)
    
    # Global emotion state
    ivy_emotion_state = CharacterEmotionState()

# Define Live2D character
# Note: Path is relative to the game directory
image ivy_live2d_base = Live2D("../../Ivy/Ivy.model3.json", 
    top=0.1, 
    base=0.6,
    height=1.7,
    loop=True,
    seamless=True)

# Screen for displaying Live2D character
screen live2d_character(emotion="neutral", xpos=0.5, ypos=1.0):
    
    python:
        # Update emotion if changed
        new_motion = ivy_emotion_state.set_emotion(emotion)
        motion_path = ivy_emotion_state.get_current_motion_path()
    
    # Display Live2D character
    add "ivy_live2d_base":
        xalign xpos
        yalign ypos
        zoom 0.5  # Adjust size as needed

# Screen for Live2D with emotion indicator (for testing)
screen live2d_debug(emotion="neutral"):
    
    use live2d_character(emotion=emotion)
    
    # Debug info overlay
    frame:
        xalign 0.0
        yalign 0.0
        padding (10, 10)
        has vbox spacing 5
        
        text "Live2D Debug Info" size 16 color "#00ff00"
        text "Current Emotion: [emotion]" size 14
        text "Current Motion: [ivy_emotion_state.current_motion]" size 14
        
        if live2d_bridge_loaded:
            text "Bridge: Loaded" size 14 color "#00ff00"
        else:
            text "Bridge: Fallback Mode" size 14 color "#ffff00"

# Transform for Live2D animations
transform live2d_bounce:
    ease 0.5 yoffset -20
    ease 0.5 yoffset 0
    repeat

transform live2d_shake:
    ease 0.1 xoffset -5
    ease 0.1 xoffset 5
    ease 0.1 xoffset 0

# Helper function to play motion with emotion
init python:
    def play_emotion_motion(emotion):
        """Play motion corresponding to emotion."""
        motion = get_motion_for_emotion(emotion)
        motion_path = get_motion_path(motion)
        
        # Note: In actual implementation, you'd call the Live2D motion play method
        # This depends on the Ren'Py Live2D plugin being properly configured
        ivy_emotion_state.set_emotion(emotion)
        
        # Return motion name for confirmation
        return motion
    
    def apply_emotion_parameters(emotion):
        """Apply Live2D parameters for emotion."""
        params = get_parameters_for_emotion(emotion)
        
        # Note: In actual implementation, you'd set Live2D parameters
        # This requires the Live2D plugin's parameter setting methods
        for param_id, value in params.items():
            # Would set parameter on character here
            pass
        
        return params