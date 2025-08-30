# Live2D Motion Testing Scene

label live2d_test:
    scene black
    
    $ quick_menu = False
    
    system "=== Live2D Motion Test Scene ==="
    system "Testing emotion to motion mappings..."
    
    # Show Live2D character with debug info
    show screen live2d_debug("neutral")
    
    narrator "Ivy appears on screen with neutral expression."
    
    menu live2d_test_menu:
        "Test Basic Emotions":
            jump test_basic_emotions
            
        "Test Complex Emotions":
            jump test_complex_emotions
            
        "Test All Motions Directly":
            jump test_all_motions
            
        "Test Emotion Transitions":
            jump test_emotion_transitions
            
        "View Emotion Mappings":
            jump view_emotion_mappings
            
        "Return to Main Menu":
            hide screen live2d_debug
            $ quick_menu = True
            return

label test_basic_emotions:
    system "Testing basic emotions..."
    
    # Test each basic emotion
    python:
        basic_emotions = [
            ("happy", "Ivy looks happy!"),
            ("sad", "Ivy looks sad..."),
            ("angry", "Ivy looks angry!"),
            ("surprised", "Ivy looks surprised!"),
            ("nervous", "Ivy looks nervous..."),
            ("shy", "Ivy looks shy..."),
            ("excited", "Ivy looks excited!"),
            ("neutral", "Ivy returns to neutral.")
        ]
    
    $ emotion_index = 0
    
    label basic_emotion_loop:
        $ current_emotion, description = basic_emotions[emotion_index]
        
        hide screen live2d_debug
        show screen live2d_debug(current_emotion)
        
        narrator "[description]"
        
        python:
            motion = get_motion_for_emotion(current_emotion)
            params = get_parameters_for_emotion(current_emotion)
            param_count = len(params)
        
        system "Emotion: [current_emotion] → Motion: [motion]"
        if param_count > 0:
            system "Applied [param_count] parameter adjustments"
        
        menu:
            "Next Emotion" if emotion_index < len(basic_emotions) - 1:
                $ emotion_index += 1
                jump basic_emotion_loop
                
            "Previous Emotion" if emotion_index > 0:
                $ emotion_index -= 1
                jump basic_emotion_loop
                
            "Back to Test Menu":
                jump live2d_test_menu

label test_complex_emotions:
    system "Testing complex emotional states..."
    
    python:
        complex_emotions = [
            ("embarrassed", "Ivy looks embarrassed!"),
            ("flustered", "Ivy is flustered!"),
            ("determined", "Ivy looks determined."),
            ("confused", "Ivy seems confused?"),
            ("playful", "Ivy is being playful~"),
            ("sarcastic", "Ivy gives a sarcastic look."),
            ("thinking", "Ivy is deep in thought..."),
            ("curious", "Ivy looks curious!")
        ]
    
    $ emotion_index = 0
    
    label complex_emotion_loop:
        $ current_emotion, description = complex_emotions[emotion_index]
        
        hide screen live2d_debug
        show screen live2d_debug(current_emotion)
        
        narrator "[description]"
        
        python:
            motion = get_motion_for_emotion(current_emotion)
            mapping = get_live2d_bridge().get_emotion_info(current_emotion)
            if mapping:
                fallbacks = ", ".join(mapping.fallback_motions)
            else:
                fallbacks = "none"
        
        system "Emotion: [current_emotion] → Motion: [motion]"
        system "Fallback chain: [fallbacks]"
        
        menu:
            "Next Emotion" if emotion_index < len(complex_emotions) - 1:
                $ emotion_index += 1
                jump complex_emotion_loop
                
            "Previous Emotion" if emotion_index > 0:
                $ emotion_index -= 1
                jump complex_emotion_loop
                
            "Back to Test Menu":
                jump live2d_test_menu

label test_all_motions:
    system "Testing all available motion files directly..."
    
    python:
        available_motions = [
            "idle", "happy", "excited", "shy", "nervous",
            "upset", "hmph", "disagreement", "neutral", "dancing"
        ]
    
    $ motion_index = 0
    
    label motion_loop:
        $ current_motion = available_motions[motion_index]
        
        # For direct motion testing, we use the motion as emotion
        hide screen live2d_debug
        show screen live2d_debug(current_motion)
        
        narrator "Playing motion: [current_motion]"
        
        $ motion_file = f"../Ivy/motion/{current_motion}.motion3.json"
        system "Motion file: [motion_file]"
        
        menu:
            "Next Motion" if motion_index < len(available_motions) - 1:
                $ motion_index += 1
                jump motion_loop
                
            "Previous Motion" if motion_index > 0:
                $ motion_index -= 1
                jump motion_loop
                
            "Back to Test Menu":
                jump live2d_test_menu

label test_emotion_transitions:
    system "Testing smooth emotion transitions..."
    
    narrator "Watch Ivy transition through different emotional states."
    
    # Happy sequence
    hide screen live2d_debug
    show screen live2d_debug("neutral")
    narrator "Starting from neutral..."
    pause 1.0
    
    hide screen live2d_debug
    show screen live2d_debug("happy")
    narrator "Ivy becomes happy!"
    pause 1.5
    
    hide screen live2d_debug
    show screen live2d_debug("excited")
    narrator "Now she's excited!"
    pause 1.5
    
    # Shy sequence
    hide screen live2d_debug
    show screen live2d_debug("shy")
    narrator "Suddenly shy..."
    pause 1.5
    
    hide screen live2d_debug
    show screen live2d_debug("embarrassed")
    narrator "And embarrassed!"
    pause 1.5
    
    # Negative sequence
    hide screen live2d_debug
    show screen live2d_debug("annoyed")
    narrator "Getting annoyed..."
    pause 1.5
    
    hide screen live2d_debug
    show screen live2d_debug("angry")
    narrator "Now angry!"
    pause 1.5
    
    hide screen live2d_debug
    show screen live2d_debug("upset")
    narrator "Becoming upset..."
    pause 1.5
    
    # Return to neutral
    hide screen live2d_debug
    show screen live2d_debug("neutral")
    narrator "Back to neutral."
    
    jump live2d_test_menu

label view_emotion_mappings:
    system "=== Emotion to Motion Mappings ==="
    
    python:
        bridge = get_live2d_bridge()
        all_emotions = sorted(bridge.get_emotion_list())
        
        # Group emotions by category
        positive = ["happy", "excited", "joyful", "content", "playful"]
        shy_group = ["shy", "embarrassed", "flustered"]
        nervous_group = ["nervous", "anxious", "worried"]
        negative = ["angry", "annoyed", "frustrated", "upset", "sad"]
        neutral_group = ["neutral", "thinking", "curious", "confused", "determined"]
        
    system "Positive Emotions:"
    python:
        for emotion in positive:
            if emotion in all_emotions:
                motion = get_motion_for_emotion(emotion)
                renpy.say(None, f"  • {emotion} → {motion}")
    
    system "\nShy/Embarrassed Emotions:"
    python:
        for emotion in shy_group:
            if emotion in all_emotions:
                motion = get_motion_for_emotion(emotion)
                renpy.say(None, f"  • {emotion} → {motion}")
    
    system "\nNervous/Anxious Emotions:"
    python:
        for emotion in nervous_group:
            if emotion in all_emotions:
                motion = get_motion_for_emotion(emotion)
                renpy.say(None, f"  • {emotion} → {motion}")
    
    system "\nNegative Emotions:"
    python:
        for emotion in negative:
            if emotion in all_emotions:
                motion = get_motion_for_emotion(emotion)
                renpy.say(None, f"  • {emotion} → {motion}")
    
    system "\nNeutral/Contemplative Emotions:"
    python:
        for emotion in neutral_group:
            if emotion in all_emotions:
                motion = get_motion_for_emotion(emotion)
                renpy.say(None, f"  • {emotion} → {motion}")
    
    system "\nTotal supported emotions: [all_emotions.__len__()]"
    
    jump live2d_test_menu