# Live2D test script to verify model loading

init python:
    import os
    
    # Check if Live2D model exists
    model_path = os.path.join(config.basedir, "..", "Ivy", "Ivy.model3.json")
    if os.path.exists(model_path):
        print(f"Live2D model found at: {model_path}")
        
        # List available motions
        motion_dir = os.path.join(config.basedir, "..", "Ivy", "motion")
        if os.path.exists(motion_dir):
            motions = [f for f in os.listdir(motion_dir) if f.endswith('.motion3.json')]
            print(f"Available motions: {motions}")
    else:
        print(f"Live2D model NOT found at: {model_path}")

# Define Live2D displayable
image ivy base = Live2D("assets/live2d/Ivy/Ivy.model3.json", base=.6, height=1.7, top=.1)
image ivy idle = Live2D("assets/live2d/Ivy/Ivy.model3.json", base=.6, height=1.7, top=.1, motion="motion/idle.motion3.json")
image ivy happy = Live2D("assets/live2d/Ivy/Ivy.model3.json", base=.6, height=1.7, top=.1, motion="motion/happy.motion3.json")
image ivy excited = Live2D("assets/live2d/Ivy/Ivy.model3.json", base=.6, height=1.7, top=.1, motion="motion/excited.motion3.json")

# Test label
label test_live2d:
    scene black
    
    "Testing Live2D model loading..."
    
    show ivy base
    "Base Ivy model loaded."
    
    show ivy idle
    "Idle motion applied."
    
    show ivy happy
    "Happy motion applied."
    
    show ivy excited  
    "Excited motion applied."
    
    "Live2D test complete!"
    return