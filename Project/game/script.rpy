# Dynamic CYOA Visual Novel - Main Script
# Clean and organized version

init python:
    import sys
    import os
    
    # Add AI module to path
    if "game/ai" not in sys.path:
        sys.path.append(os.path.join(config.gamedir, "ai"))
    
    # Import core modules
    try:
        from config import get_config
        from api import APIClient
        from cache import get_cache_manager
        from state import get_game_state
        
        # Initialize configuration
        ai_config = get_config()
        api_client = APIClient(ai_config)
        cache_manager = get_cache_manager()
        game_state = get_game_state()
        
        # Success flag
        infrastructure_loaded = True
        load_error = None
        
    except Exception as e:
        infrastructure_loaded = False
        load_error = str(e)
        ai_config = None
        api_client = None
        cache_manager = None
        game_state = None

define narrator = Character(None, what_style="say_thought")
define system = Character("System", color="#00ff00")

label start:
    scene black
    
    if not infrastructure_loaded:
        system "ERROR: Infrastructure failed to load!"
        system "Error details: [load_error]"
        system "Please check the Python modules in game/ai/"
        return
    
    system "Welcome to the Dynamic CYOA Visual Novel Test Suite"
    system "All infrastructure components loaded successfully!"
    
    label main_menu_loop:
        menu:
            "Live2D Testing (Haru - Working Model)":
                call live2d_haru_menu
                jump main_menu_loop
                
            "Live2D Testing (Ivy - Static Model)":
                call live2d_ivy_menu
                jump main_menu_loop
                
            "TTS Audio Testing":
                call tts_simple_test
                jump main_menu_loop
                
            "API and Infrastructure Testing":
                call infrastructure_menu
                jump main_menu_loop
                
            "View System Status":
                call system_status
                jump main_menu_loop
                
            "Exit":
                pass  # Don't jump back to menu
        
    system "Thank you for testing!"
    return

# Haru Live2D Menu (Working)
label live2d_haru_menu:
    menu:
        "Haru Live2D Tests"
        
        "Demo Scene":
            system "Starting Haru demo scene..."
            call haru_demo_scene
            
        "Interactive Test":
            system "Starting Haru interactive test..."
            call test_haru_interactive
            
        "Simple Test":
            system "Testing Haru basic functionality..."
            call test_haru_simple
            
        "Motion Groups Test":
            system "Testing Haru motion groups..."
            call test_haru_groups
            
        "Back":
            return
    
    jump live2d_haru_menu

# Ivy Live2D Menu (Static)
label live2d_ivy_menu:
    menu:
        "Ivy Live2D Tests (Note: Model is static due to missing motion references)"
        
        "Basic Test":
            system "Testing Ivy Live2D..."
            call live2d_test
            
        "Debug Test":
            system "Testing with debug enabled..."
            call test_live2d_debug
            
        "Motion Info":
            system "Checking motion discovery..."
            call test_live2d_with_info
            
        "Back":
            return
    
    jump live2d_ivy_menu


# Infrastructure Menu
label infrastructure_menu:
    menu:
        "Infrastructure and API Testing"
        
        "Test API Connection":
            system "Testing API connectivity..."
            python:
                try:
                    response = api_client.get("/health")
                    if response.success:
                        api_status = "API connection successful!"
                    else:
                        api_status = f"API returned status: {response.status_code}"
                except Exception as e:
                    api_status = f"API error: {str(e)}"
            system "[api_status]"
            
        "Test Text Generation":
            system "Testing text generation..."
            python:
                try:
                    result = api_client.generate_text(
                        prompt="Say 'Hello, dynamic CYOA world!' in a creative way.",
                        temperature=0.7,
                        max_tokens=50
                    )
                    if result:
                        gen_text = result
                    else:
                        gen_text = "Text generation failed - no response"
                except Exception as e:
                    gen_text = f"Generation error: {str(e)}"
            narrator "[gen_text]"
            
        "Test State Management":
            $ game_state.set_world_fact("test_fact", "State management working")
            $ test_fact = game_state.get_world_fact("test_fact")
            system "State test: [test_fact]"
            
        "View Cache Statistics":
            $ cache_stats = cache_manager.get_cache_stats()
            $ cache_info = f"Cache files: {cache_stats['total_files']}, Size: {cache_stats['total_size']} bytes"
            system "Cache: [cache_info]"
            
        "Back":
            return
    
    jump infrastructure_menu

# System Status
label system_status:
    python:
        import os
        from datetime import datetime
        
        status_lines = []
        status_lines.append("=== System Status ===")
        status_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        status_lines.append("")
        
        status_lines.append("Phase 1: Core Infrastructure ✓")
        status_lines.append("  • Configuration module (config.py)")
        status_lines.append("  • HTTP client with retry logic (api.py)")
        status_lines.append("  • Content-based caching (cache.py)")
        status_lines.append("  • Save-compatible state management (state.py)")
        status_lines.append("")
        
        status_lines.append("Phase 2: Live2D Integration ✓")
        status_lines.append("  • Haru model (WORKING with animations)")
        status_lines.append("  • Ivy model (STATIC - missing motion refs)")
        status_lines.append("  • Emotion mapping system")
        status_lines.append("  • Motion test scenes")
        status_lines.append("")
        
        status_lines.append("Phase 3: TTS Integration ✓")
        status_lines.append("  • Audio cache system (audio_cache.py)")
        status_lines.append("  • TTS generation with caching")
        status_lines.append("  • Voice selection (7 Kokoro voices)")
        status_lines.append("  • Prefetch mechanism")
        status_lines.append("")
        
        if ai_config:
            status_lines.append(f"Configuration: API URL: {ai_config.api_base_url}")
        else:
            status_lines.append("Configuration: Not loaded")
        
        status_lines.append("")
        status_lines.append("Active Files:")
        status_lines.append("  • script.rpy - Main game script")
        status_lines.append("  • haru_live2d.rpy - Haru Live2D implementation")
        status_lines.append("  • audio_tts.rpy - TTS playback system")
        status_lines.append("  • tts_settings_simple.rpy - Voice selection UI")
        status_lines.append("  • options.rpy - Game options")
        
        # Write to file
        status_file = os.path.join(os.path.dirname(config.gamedir), "systemstatus.txt")
        with open(status_file, 'w') as f:
            f.write('\n'.join(status_lines))
        
        # Also display in game
        for line in status_lines:
            system(line)
        
        system(f"\nStatus written to: {status_file}")
    
    return

# Simplified TTS test
label tts_simple_test:
    system "TTS Testing"
    
    menu:
        "Test Voice Playback":
            python:
                test_text = "Hello! This is a test of the text-to-speech system."
                success = play_tts_line(test_text, voice="af_bella", wait=False)
                if success:
                    narrator("Playing TTS audio...")
                else:
                    narrator("TTS playback failed - check API configuration")
            narrator "[test_text]"
            pause 2.0
            
        "Open Voice Settings":
            show screen tts_settings_simple
            
        "Back":
            return
    
    jump tts_simple_test

# Simplified Haru test
label test_haru_simple:
    scene black
    show haru
    "Haru is displayed with idle animation."
    
    $ haru.do("g_m01")
    "Motion: g_m01"
    
    $ haru.do("g_idle") 
    "Back to idle"
    
    hide haru
    return


# Test motion groups
label test_haru_groups:
    scene black
    show haru
    
    "Testing motion groups..."
    
    python:
        motions = ["g_idle", "g_m01", "g_m02", "g_m03"]
        for motion in motions:
            haru.do(motion)
            narrator(f"Playing motion: {motion}")
            renpy.pause(1.5)
    
    hide haru
    return

# Simple Ivy test (static model)
label live2d_test:
    scene black
    "Note: Ivy model is static due to missing motion references in model3.json"
    "Displaying Ivy model..."
    
    # Try to show Ivy if defined
    # show ivy
    "Ivy would appear here if motion references were fixed."
    
    return

# Debug test for Ivy
label test_live2d_debug:
    scene black
    "Debug mode for Ivy Live2D (currently static)"
    "Check console for debug output if enabled."
    return

# Motion info for Ivy
label test_live2d_with_info:
    scene black
    "Ivy Motion Discovery Info:"
    "The Ivy model lacks a 'Motions' section in Ivy.model3.json"
    "Motion files exist in Ivy/motions/ but aren't referenced"
    "This causes the model to appear static"
    return