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
                call tts_menu
                jump main_menu_loop
                
            "API and Infrastructure Testing":
                call infrastructure_menu
                jump main_menu_loop
                
            "View System Status":
                call system_status
                jump main_menu_loop
                
            "Exit":
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

# TTS Menu
label tts_menu:
    menu:
        "Text-to-Speech Testing"
        
        "Full TTS Test":
            system "Launching TTS test suite..."
            call tts_test
            
        "Voice Selection Menu":
            system "Opening voice selection menu..."
            call tts_voice_menu
            
        "Voice Settings Screen":
            show screen tts_settings_simple
            
        "Back":
            return
    
    jump tts_menu

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
    system "=== System Status ==="
    
    system "Phase 1: Core Infrastructure ✓"
    system "  • Configuration module (config.py)"
    system "  • HTTP client with retry logic (api.py)"
    system "  • Content-based caching (cache.py)"
    system "  • Save-compatible state management (state.py)"
    
    system "Phase 2: Live2D Integration ✓"
    system "  • Haru model (WORKING with animations)"
    system "  • Ivy model (STATIC - missing motion refs)"
    system "  • Emotion mapping system"
    system "  • Motion test scenes"
    
    system "Phase 3: TTS Integration ✓"
    system "  • Audio cache system (audio_cache.py)"
    system "  • TTS generation with caching"
    system "  • Voice selection (7 Kokoro voices)"
    system "  • Prefetch mechanism"
    
    $ config_info = f"API URL: {ai_config.api_base_url}"
    system "Configuration: [config_info]"
    
    return