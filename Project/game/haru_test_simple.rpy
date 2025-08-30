# Simple Haru test to discover available attributes

# Define Haru with debug enabled
define config.log_live2d_loading = True

image haru_test = Live2D("assets/live2d/Haru/Haru.model3.json",
    base=0.8,
    height=1.0,
    loop=True)

label test_haru_simple:
    scene black
    
    system "=== Simple Haru Test ==="
    narrator "Testing what attributes are actually available..."
    
    # Show base Haru
    show haru_test at Transform(xalign=0.5, yalign=1.0)
    "Haru loaded. Check log.txt for available motions/expressions."
    
    # The model has "Idle" and "TapBody" groups in the JSON
    # Try the group names directly
    show haru_test idle
    "Trying 'idle' attribute..."
    pause 2.0
    
    show haru_test tapbody
    "Trying 'tapbody' attribute..."  
    pause 2.0
    
    # Try without any motion (still)
    show haru_test still
    "Using 'still' to stop motion..."
    pause 2.0
    
    # Try expressions with their original names
    show haru_test f01
    "Trying expression 'f01'..."
    pause 2.0
    
    show haru_test f02
    "Trying expression 'f02'..."
    pause 2.0
    
    hide haru_test
    
    narrator "Test complete. Check log.txt for Live2D loading details."
    
    return

# Test to see if motion group names work
label test_haru_groups:
    scene black
    
    system "=== Testing Motion Groups ==="
    
    show haru at Transform(xalign=0.5, yalign=1.0)
    haru "Testing with motion group names from model3.json..."
    
    # The model defines two groups: "Idle" and "TapBody"
    # Try lowercase versions
    show haru idle
    haru "Trying 'idle' (motion group)..."
    pause 2.0
    
    show haru tapbody  
    haru "Trying 'tapbody' (motion group)..."
    pause 2.0
    
    # Try the special attributes
    show haru still
    haru "Using 'still' to stop all motion..."
    pause 2.0
    
    show haru null
    haru "Using 'null' for default expression..."
    pause 2.0
    
    hide haru
    return