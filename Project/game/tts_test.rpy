# TTS Testing Scene

label tts_test:
    scene black
    
    $ quick_menu = False
    
    system "=== TTS Audio Test Scene ==="
    system "Testing text-to-speech with caching..."
    
    # Check if TTS system is loaded
    if not tts_system_loaded:
        system "ERROR: TTS system not loaded!"
        system "Please check audio_cache.py and API configuration."
        $ quick_menu = True
        return
    
    narrator "TTS system loaded successfully."
    
    menu tts_test_menu:
        "Test Single Line":
            jump test_single_tts
            
        "Test Multiple Voices":
            jump test_voice_variety
            
        "Test Dialog with Emotions":
            jump test_dialog_emotions
            
        "Test Caching Behavior":
            jump test_tts_cache
            
        "Test Prefetch Mechanism":
            jump test_prefetch
            
        "Configure TTS Voice":
            show screen tts_settings
            jump tts_test_menu
            
        "View Cache Statistics":
            jump view_cache_stats
            
        "Return to Main Menu":
            $ quick_menu = True
            return

label test_single_tts:
    system "Testing single TTS line..."
    
    python:
        test_text = "Hello! This is a test of the text-to-speech system. Can you hear me clearly?"
        narrator("Playing TTS audio...")
        
        # Play TTS line with Kokoro voice
        success = play_tts_line(test_text, voice="af_bella", wait=True)
        
        if success:
            result_msg = "TTS playback successful!"
        else:
            result_msg = "TTS playback failed - check API configuration"
    
    system "[result_msg]"
    narrator "[test_text]"
    
    jump tts_test_menu

label test_voice_variety:
    system "Testing different TTS voices..."
    
    python:
        voices_to_test = [
            ("af_sky", "I'm Sky, with a cheerful British accent."),
            ("af_bella", "I'm Bella, an American voice that's friendly."),
            ("af_nicole", "I'm Nicole, warm and welcoming."),
            ("am_adam", "I'm Adam, professional and clear."),
            ("am_michael", "I'm Michael, calm and steady."),
            ("bf_emma", "I'm Emma, elegant with a British touch."),
            ("bm_george", "I'm George, authoritative and British.")
        ]
    
    $ voice_index = 0
    
    label voice_loop:
        $ current_voice, current_text = voices_to_test[voice_index]
        
        system "Testing voice: [current_voice]"
        
        python:
            # Play TTS with current voice
            success = play_tts_line(current_text, voice=current_voice, wait=False)
            
            if success:
                status = f"Playing {current_voice}..."
            else:
                status = f"Failed to play {current_voice}"
        
        narrator "[status]"
        narrator "[current_text]"
        
        # Wait for audio to finish
        if success:
            pause 2.0  # Give time for audio to play
        
        menu:
            "Next Voice" if voice_index < len(voices_to_test) - 1:
                $ voice_index += 1
                jump voice_loop
                
            "Previous Voice" if voice_index > 0:
                $ voice_index -= 1
                jump voice_loop
                
            "Back to Test Menu":
                jump tts_test_menu

label test_dialog_emotions:
    system "Testing dialog with TTS and emotions..."
    
    # Show Live2D character if available
    if 'ivy_emotion_state' in dir():
        show screen live2d_character("neutral")
        narrator "Live2D character shown with emotions."
    else:
        narrator "Live2D not available - testing TTS only."
    
    # Character for dialog
    define ivy = Character("Ivy", color="#c8a2c8")
    
    python:
        dialog_sequence = [
            ("neutral", "Hello! I'm testing the TTS system with different emotions.", "af_bella"),
            ("happy", "When I'm happy, my voice might sound more cheerful!", "af_sky"),
            ("sad", "And when I'm sad, it might be more subdued...", "af_nicole"),
            ("excited", "But when I'm excited, everything sounds amazing!", "af_sky"),
            ("thinking", "Hmm, let me think about that for a moment...", "bf_emma"),
            ("surprised", "Oh! I didn't expect that to happen!", "af_bella"),
            ("nervous", "I'm a bit nervous about this test...", "af_nicole"),
            ("determined", "But I'm determined to make it work perfectly!", "am_adam"),
            ("playful", "Let's have some fun with this system!", "af_sky"),
            ("neutral", "That concludes our emotion test. Thank you!", "af_bella")
        ]
    
    $ dialog_index = 0
    
    label emotion_dialog_loop:
        $ emotion, text, voice = dialog_sequence[dialog_index]
        
        # Update emotion if Live2D available
        if 'ivy_emotion_state' in dir():
            hide screen live2d_character
            show screen live2d_character(emotion)
        
        system "Emotion: [emotion], Voice: [voice]"
        
        # Play dialog with TTS
        python:
            success = play_tts_line(text, voice=voice, wait=False)
        
        ivy "[text]"
        
        # Wait for audio if playing
        if success:
            pause 2.0  # Give time for audio to play
        
        menu:
            "Next Line" if dialog_index < len(dialog_sequence) - 1:
                $ dialog_index += 1
                jump emotion_dialog_loop
                
            "Previous Line" if dialog_index > 0:
                $ dialog_index -= 1
                jump emotion_dialog_loop
                
            "Back to Test Menu":
                hide screen live2d_character
                jump tts_test_menu

label test_tts_cache:
    system "Testing TTS caching behavior..."
    
    python:
        import time
        
        # Test text for caching
        cache_test_text = "This line will be used to test caching. It should be faster the second time!"
        
        narrator("First generation (should be slower)...")
        
        # Clear any existing cache for this text
        cache = get_audio_cache()
        if cache.verify_cache(cache_test_text, "af_bella"):
            narrator("(Clearing existing cache entry...)")
            # Note: In production, we'd have a method to remove specific entries
        
        # Time first generation
        start_time = time.time()
        success1 = play_tts_line(cache_test_text, voice="af_bella", wait=True)
        time1 = time.time() - start_time
        
        if success1:
            result1 = f"First play: {time1:.2f} seconds (generated)"
        else:
            result1 = "First play: Failed"
        
        narrator(result1)
    
    pause 1.0
    
    python:
        narrator("Second play (should use cache)...")
        
        # Time cached playback
        start_time = time.time()
        success2 = play_tts_line(cache_test_text, voice="af_bella", wait=True)
        time2 = time.time() - start_time
        
        if success2:
            result2 = f"Second play: {time2:.2f} seconds (cached)"
            if time2 < time1:
                cache_status = "✓ Cache is working! Second play was faster."
            else:
                cache_status = "⚠ Cache might not be working properly."
        else:
            result2 = "Second play: Failed"
            cache_status = "✗ Cache test failed"
        
        narrator(result2)
        narrator(cache_status)
    
    system "Cache test complete."
    
    jump tts_test_menu

label test_prefetch:
    system "Testing TTS prefetch mechanism..."
    
    python:
        prefetch_lines = [
            "This is the first line that will play immediately.",
            "This second line is being prefetched while the first plays.",
            "The third line is prefetched during the second.",
            "And finally, the fourth line completes our test."
        ]
        
        narrator("Starting prefetch test...")
        
        # Play first line and prefetch second
        play_tts_line(prefetch_lines[0], voice="af_bella", wait=False)
        prefetch_next_tts(prefetch_lines[1], voice="af_bella")
        
        narrator(prefetch_lines[0])
        # Audio plays asynchronously
        
        # Play second line and prefetch third
        play_tts_line(prefetch_lines[1], voice="af_bella", wait=False)
        prefetch_next_tts(prefetch_lines[2], voice="af_bella")
        
        narrator(prefetch_lines[1])
        # Audio plays asynchronously
        
        # Play third line and prefetch fourth
        play_tts_line(prefetch_lines[2], voice="af_bella", wait=False)
        prefetch_next_tts(prefetch_lines[3], voice="af_bella")
        
        narrator(prefetch_lines[2])
        # Audio plays asynchronously
        
        # Play fourth line
        play_tts_line(prefetch_lines[3], voice="af_bella", wait=False)
        
        narrator(prefetch_lines[3])
        # Audio plays asynchronously
    
    system "Prefetch test complete."
    system "Lines should have played smoothly with minimal gaps."
    
    jump tts_test_menu

label view_cache_stats:
    system "=== TTS Cache Statistics ==="
    
    python:
        cache_info = tts_manager.get_cache_info()
        
        stats_text = f"""
        Cache Directory: {cache_info['cache_dir']}
        Total Files: {cache_info['total_files']}
        Total Size: {cache_info['total_size_mb']} MB
        """
        
        for line in stats_text.strip().split('\n'):
            renpy.say(None, line.strip())
    
    menu:
        "Clear Cache":
            python:
                files_removed = clear_tts_cache()
                clear_msg = f"Removed {files_removed} cached files."
            system "[clear_msg]"
            jump view_cache_stats
            
        "Back to Test Menu":
            jump tts_test_menu