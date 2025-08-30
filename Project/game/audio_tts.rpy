# TTS Audio Integration for Ren'Py

init python:
    import os
    import sys
    import threading
    from pathlib import Path
    
    # Add AI module to path if needed
    if "game/ai" not in sys.path:
        sys.path.append(os.path.join(config.gamedir, "ai"))
    
    # Import audio cache system
    try:
        from audio_cache import (
            get_or_generate_tts,
            prefetch_tts,
            clear_tts_cache,
            get_audio_cache
        )
        tts_system_loaded = True
    except ImportError as e:
        tts_system_loaded = False
        print(f"Warning: Could not load TTS system: {e}")
        # Fallback functions
        def get_or_generate_tts(text, voice=None):
            return None
        def prefetch_tts(text, voice=None):
            return False
        def clear_tts_cache():
            return 0
    
    # TTS playback state
    class TTSPlaybackManager:
        def __init__(self):
            self.current_text = ""
            self.current_voice = "af_bella"
            self.is_playing = False
            self.prefetch_queue = []
            self.playback_channel = "voice"
            self.fallback_sound = None
            
        def play_tts_line(self, text, voice="alloy", wait=True):
            """Play a TTS line with caching.
            
            Args:
                text: Text to speak
                voice: Voice to use
                wait: Whether to wait for completion
                
            Returns:
                True if playing, False if failed
            """
            self.current_text = text
            self.current_voice = voice
            
            # Get or generate TTS audio
            audio_path = get_or_generate_tts(text, voice)
            
            if audio_path and os.path.exists(audio_path):
                # Play the audio using renpy.sound
                renpy.sound.play(audio_path)
                self.is_playing = True
                
                if wait:
                    # Wait for audio to finish (simplified approach)
                    pass
                    
                return True
            else:
                # Fallback to text-only with optional sound effect
                if self.fallback_sound:
                    renpy.sound.play(self.fallback_sound)
                return False
        
        def stop_tts(self):
            """Stop current TTS playback."""
            renpy.sound.stop()
            self.is_playing = False
        
        def prefetch_next_line(self, text, voice="alloy"):
            """Prefetch TTS for next line.
            
            Args:
                text: Text to prefetch
                voice: Voice to use
            """
            # Start prefetch in background
            threading.Thread(
                target=lambda: prefetch_tts(text, voice),
                daemon=True
            ).start()
        
        def set_fallback_sound(self, sound_path):
            """Set fallback sound for when TTS fails.
            
            Args:
                sound_path: Path to fallback sound effect
            """
            self.fallback_sound = sound_path
        
        def get_cache_info(self):
            """Get TTS cache information.
            
            Returns:
                Dict with cache statistics
            """
            if tts_system_loaded:
                cache = get_audio_cache()
                return cache.get_cache_stats()
            else:
                return {
                    "cache_dir": "N/A",
                    "total_files": 0,
                    "total_size_mb": 0
                }
    
    # Global TTS manager
    tts_manager = TTSPlaybackManager()
    
    # Convenience function for Ren'Py scripts
    def play_tts_line(text, voice="alloy", wait=True):
        """Play TTS line with caching support.
        
        Args:
            text: Text to speak
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            wait: Whether to wait for completion
            
        Returns:
            True if playing, False if failed
        """
        return tts_manager.play_tts_line(text, voice, wait)
    
    def stop_tts():
        """Stop current TTS playback."""
        tts_manager.stop_tts()
    
    def prefetch_next_tts(text, voice="alloy"):
        """Prefetch TTS for next line."""
        tts_manager.prefetch_next_line(text, voice)
    
    # Advanced playback with emotion integration
    def play_dialog_with_tts(character_name, text, emotion="neutral", voice="alloy"):
        """Play dialog line with TTS and Live2D emotion.
        
        Args:
            character_name: Character speaking
            text: Dialog text
            emotion: Live2D emotion
            voice: TTS voice
        """
        # Update Live2D emotion if available
        if hasattr(store, 'ivy_emotion_state'):
            store.ivy_emotion_state.set_emotion(emotion)
        
        # Play TTS
        success = play_tts_line(text, voice, wait=False)
        
        # Show text with character
        if character_name:
            renpy.say(character_name, text)
        else:
            renpy.say(None, text)
        
        # Wait for TTS to finish if it was playing
        if success:
            pass  # Audio plays asynchronously
    
    # Batch TTS generation for entire scenes
    def prefetch_scene_dialog(dialog_lines):
        """Prefetch TTS for multiple dialog lines.
        
        Args:
            dialog_lines: List of (text, voice) tuples
        """
        for text, voice in dialog_lines:
            prefetch_tts(text, voice)
    
    # TTS voice selection helper
    class TTSVoiceSelector:
        """Helper for selecting and previewing TTS voices."""
        
        AVAILABLE_VOICES = [
            ("af_sky", "Sky - British female, cheerful"),
            ("af_bella", "Bella - American female, friendly"),
            ("af_nicole", "Nicole - American female, warm"),
            ("am_adam", "Adam - American male, professional"),
            ("am_michael", "Michael - American male, calm"),
            ("bf_emma", "Emma - British female, elegant"),
            ("bm_george", "George - British male, authoritative")
        ]
        
        def __init__(self):
            self.selected_voice = "af_bella"
            self.preview_text = "Hello! This is how I sound."
        
        def set_voice(self, voice):
            """Set the selected voice."""
            self.selected_voice = voice
        
        def preview_voice(self, voice=None):
            """Preview a voice with sample text."""
            voice = voice or self.selected_voice
            play_tts_line(self.preview_text, voice)
        
        def get_voice_description(self, voice):
            """Get description for a voice."""
            for v, desc in self.AVAILABLE_VOICES:
                if v == voice:
                    return desc
            return "Unknown voice"
    
    # Global voice selector
    tts_voice_selector = TTSVoiceSelector()

# Voice channel registration removed - using renpy.sound instead

# Screen for TTS settings
screen tts_settings():
    modal True
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        ysize 500
        
        vbox:
            spacing 10
            
            text "TTS Voice Settings" size 28 xalign 0.5 color "#ffffff"
            
            null height 20
            
            text "Select Voice:" size 20 color "#cccccc"
            
            null height 10
            
            # Voice selection buttons
            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                ysize 200
                
                vbox:
                    spacing 5
                    
                    for voice, description in tts_voice_selector.AVAILABLE_VOICES:
                        textbutton "[voice] - [description]":
                            action [
                                Function(tts_voice_selector.set_voice, voice),
                                Function(tts_voice_selector.preview_voice, voice)
                            ]
                            text_size 16
                            text_idle_color "#aaaaaa"
                            text_hover_color "#ffffff"
                            text_selected_color "#00ff00"
                            xfill True
                            selected tts_voice_selector.selected_voice == voice
            
            null height 15
            
            # Preview text input
            text "Preview Text:" size 16 color "#cccccc"
            $ preview_text = tts_voice_selector.preview_text
            text "[preview_text]" size 14 color "#999999"
            
            # Preview button
            textbutton "Preview Selected Voice":
                action Function(tts_voice_selector.preview_voice)
                text_size 16
                text_idle_color "#aaaaaa"
                text_hover_color "#ffffff"
                xalign 0.5
            
            null height 15
            
            # Cache info
            if tts_system_loaded:
                $ cache_info = tts_manager.get_cache_info()
                $ total_files = cache_info['total_files']
                $ total_size_mb = cache_info['total_size_mb']
                text "Cache: [total_files] files, [total_size_mb] MB" size 14 color "#888888"
                
                textbutton "Clear Cache":
                    action Function(clear_tts_cache)
                    text_size 14
                    text_idle_color "#ff8888"
                    text_hover_color "#ff0000"
            else:
                text "TTS System: Not loaded" size 14 color "#ff0000"
            
            null height 20
            
            # Close button
            textbutton "Close":
                action Hide("tts_settings")
                text_size 18
                text_idle_color "#cccccc"
                text_hover_color "#ffffff"
                xalign 0.5

# Screen for TTS playback indicator
screen tts_indicator():
    if tts_manager.is_playing:
        frame:
            xalign 0.95
            yalign 0.05
            padding (5, 5)
            
            text "🔊" size 20