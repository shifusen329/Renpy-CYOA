# Options for the game

init python:
    # Disable quit confirmation to avoid Layout.yesno_prompt error
    config.quit_action = Quit(confirm=False)
    
    # Also set this for good measure
    _confirm_quit = False