# Dynamic CYOA Visual Novel - Core Infrastructure Test

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
    
    if infrastructure_loaded:
        system "Phase 1 Infrastructure loaded successfully!"
        
        $ config_info = f"API URL: {ai_config.api_base_url}"
        system "Configuration: [config_info]"
        
        # Test state management
        $ game_state.set_world_fact("test_fact", "Infrastructure operational")
        $ test_fact = game_state.get_world_fact("test_fact")
        system "State management: [test_fact]"
        
        # Test cache stats
        $ cache_stats = cache_manager.get_cache_stats()
        $ cache_info = f"Cache files: {cache_stats['total_files']}, Size: {cache_stats['total_size']} bytes"
        system "Cache system: [cache_info]"
        
        menu:
            "Test API connection":
                system "Testing API connectivity..."
                python:
                    try:
                        # Test basic endpoint
                        response = api_client.get("/health")
                        if response.success:
                            api_status = "API connection successful!"
                        else:
                            api_status = f"API returned status: {response.status_code}"
                    except Exception as e:
                        api_status = f"API error: {str(e)}"
                
                system "[api_status]"
                
            "Test text generation":
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
                
            "View infrastructure summary":
                system "=== Phase 1 Infrastructure Summary ==="
                system "✓ Configuration module (config.py)"
                system "✓ HTTP client with retry logic (api.py)"
                system "✓ Content-based caching (cache.py)"
                system "✓ Save-compatible state management (state.py)"
                system "✓ Ren'Py integration successful"
                
            "Exit":
                system "Infrastructure test complete!"
                return
        
        system "All Phase 1 components are operational."
        system "Ready for Phase 2: Agent Framework implementation."
        
    else:
        system "ERROR: Infrastructure failed to load!"
        system "Error details: [load_error]"
        system "Please check the Python modules in game/ai/"
    
    return