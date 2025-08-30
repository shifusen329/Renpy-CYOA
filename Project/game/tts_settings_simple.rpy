# Simple TTS Settings Screen that works reliably

screen tts_settings_simple():
    modal True
    
    # Dark background
    add "#000000cc"
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 650
        ysize 450
        padding (20, 20)
        
        vbox:
            spacing 15
            xfill True
            
            # Title
            text "TTS Voice Settings" size 26 xalign 0.5
            
            null height 10
            
            # Voice selection header
            text "Select Voice:" size 18
            
            # Voice buttons in a viewport for scrolling
            viewport:
                ysize 200
                scrollbars "vertical"
                mousewheel True
                
                vbox:
                    spacing 8
                    
                    # Kokoro voices
                    textbutton "af_sky - Sky - British female, cheerful":
                        action [
                            SetField(tts_voice_selector, "selected_voice", "af_sky"),
                            Function(play_tts_line, "Hello! I'm Sky with a cheerful British accent.", "af_sky", False)
                        ]
                        text_idle_color "#aaaaaa"
                        text_hover_color "#ffff00"
                        text_selected_idle_color "#ffffff"
                        text_selected_hover_color "#ffff00"
                        selected tts_voice_selector.selected_voice == "af_sky"
                        xfill True
                    
                    textbutton "af_bella - Bella - American female, friendly":
                        action [
                            SetField(tts_voice_selector, "selected_voice", "af_bella"),
                            Function(play_tts_line, "Hi! I'm Bella, friendly and American.", "af_bella", False)
                        ]
                        text_idle_color "#aaaaaa"
                        text_hover_color "#ffff00"
                        text_selected_idle_color "#ffffff"
                        text_selected_hover_color "#ffff00"
                        selected tts_voice_selector.selected_voice == "af_bella"
                        xfill True
                    
                    textbutton "af_nicole - Nicole - American female, warm":
                        action [
                            SetField(tts_voice_selector, "selected_voice", "af_nicole"),
                            Function(play_tts_line, "Hello, I'm Nicole with a warm voice.", "af_nicole", False)
                        ]
                        text_idle_color "#aaaaaa"
                        text_hover_color "#ffff00"
                        text_selected_idle_color "#ffffff"
                        text_selected_hover_color "#ffff00"
                        selected tts_voice_selector.selected_voice == "af_nicole"
                        xfill True
                    
                    textbutton "am_adam - Adam - American male, professional":
                        action [
                            SetField(tts_voice_selector, "selected_voice", "am_adam"),
                            Function(play_tts_line, "Good day. I'm Adam, professional and clear.", "am_adam", False)
                        ]
                        text_idle_color "#aaaaaa"
                        text_hover_color "#ffff00"
                        text_selected_idle_color "#ffffff"
                        text_selected_hover_color "#ffff00"
                        selected tts_voice_selector.selected_voice == "am_adam"
                        xfill True
                    
                    textbutton "am_michael - Michael - American male, calm":
                        action [
                            SetField(tts_voice_selector, "selected_voice", "am_michael"),
                            Function(play_tts_line, "Hello. I'm Michael, calm and steady.", "am_michael", False)
                        ]
                        text_idle_color "#aaaaaa"
                        text_hover_color "#ffff00"
                        text_selected_idle_color "#ffffff"
                        text_selected_hover_color "#ffff00"
                        selected tts_voice_selector.selected_voice == "am_michael"
                        xfill True
                    
                    textbutton "bf_emma - Emma - British female, elegant":
                        action [
                            SetField(tts_voice_selector, "selected_voice", "bf_emma"),
                            Function(play_tts_line, "Greetings. I'm Emma, elegant with a British touch.", "bf_emma", False)
                        ]
                        text_idle_color "#aaaaaa"
                        text_hover_color "#ffff00"
                        text_selected_idle_color "#ffffff"
                        text_selected_hover_color "#ffff00"
                        selected tts_voice_selector.selected_voice == "bf_emma"
                        xfill True
                    
                    textbutton "bm_george - George - British male, authoritative":
                        action [
                            SetField(tts_voice_selector, "selected_voice", "bm_george"),
                            Function(play_tts_line, "Good evening. I'm George, British and authoritative.", "bm_george", False)
                        ]
                        text_idle_color "#aaaaaa"
                        text_hover_color "#ffff00"
                        text_selected_idle_color "#ffffff"
                        text_selected_hover_color "#ffff00"
                        selected tts_voice_selector.selected_voice == "bm_george"
                        xfill True
            
            null height 10
            
            # Current selection display
            hbox:
                text "Selected: " size 16
                text "[tts_voice_selector.selected_voice]" size 16 color "#00ff00"
            
            # Cache info
            if tts_system_loaded:
                $ cache_info = tts_manager.get_cache_info()
                text "Cache: {0} files, {1:.1f} MB".format(
                    cache_info.get('total_files', 0),
                    cache_info.get('total_size_mb', 0)
                ) size 14 color "#888888"
            
            null height 10
            
            # Action buttons
            hbox:
                spacing 20
                xalign 0.5
                
                textbutton "Clear Cache":
                    action Function(clear_tts_cache)
                    text_idle_color "#ff8888"
                    text_hover_color "#ff0000"
                
                textbutton "Close":
                    action Hide("tts_settings_simple")
                    text_idle_color "#88ff88"
                    text_hover_color "#00ff00"