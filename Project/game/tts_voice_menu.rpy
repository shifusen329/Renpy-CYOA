# Simplified TTS Voice Selection Menu

label tts_voice_menu:
    scene black
    
    system "=== TTS Voice Selection ==="
    narrator "Choose a voice and preview it."
    
    menu voice_selection:
        "Select TTS Voice:"
        
        "Sky - British female, cheerful":
            $ tts_voice_selector.set_voice("af_sky")
            python:
                play_tts_line("Hello! I'm Sky with a cheerful British accent.", "af_sky")
            narrator "Voice set to: Sky (af_sky)"
            jump voice_selection
            
        "Bella - American female, friendly":
            $ tts_voice_selector.set_voice("af_bella")
            python:
                play_tts_line("Hi there! I'm Bella, friendly and American.", "af_bella")
            narrator "Voice set to: Bella (af_bella)"
            jump voice_selection
            
        "Nicole - American female, warm":
            $ tts_voice_selector.set_voice("af_nicole")
            python:
                play_tts_line("Hello, I'm Nicole. I have a warm American voice.", "af_nicole")
            narrator "Voice set to: Nicole (af_nicole)"
            jump voice_selection
            
        "Adam - American male, professional":
            $ tts_voice_selector.set_voice("am_adam")
            python:
                play_tts_line("Good day. I'm Adam, professional and clear.", "am_adam")
            narrator "Voice set to: Adam (am_adam)"
            jump voice_selection
            
        "Michael - American male, calm":
            $ tts_voice_selector.set_voice("am_michael")
            python:
                play_tts_line("Hello. I'm Michael, calm and steady.", "am_michael")
            narrator "Voice set to: Michael (am_michael)"
            jump voice_selection
            
        "Emma - British female, elegant":
            $ tts_voice_selector.set_voice("bf_emma")
            python:
                play_tts_line("Greetings. I'm Emma, elegant with a British touch.", "bf_emma")
            narrator "Voice set to: Emma (bf_emma)"
            jump voice_selection
            
        "George - British male, authoritative":
            $ tts_voice_selector.set_voice("bm_george")
            python:
                play_tts_line("Good evening. I'm George, British and authoritative.", "bm_george")
            narrator "Voice set to: George (bm_george)"
            jump voice_selection
            
        "Test Custom Text":
            jump tts_custom_test
            
        "Back":
            return

label tts_custom_test:
    $ custom_text = renpy.input("Enter text to test with selected voice:", default="This is a test of the selected voice.")
    
    python:
        current_voice = tts_voice_selector.selected_voice
        narrator(f"Playing with voice: {current_voice}")
        play_tts_line(custom_text, current_voice)
    
    narrator "[custom_text]"
    
    jump voice_selection