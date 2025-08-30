# Haru Live2D Implementation
# Using the properly configured demo model

# Define Haru Live2D with proper path and scaling
image haru = Live2D("assets/live2d/Haru/Haru.model3.json",
    base=0.8,  # Move base point down
    height=1.0,  # Reduce height to prevent stretching
    loop=True,
    seamless=True,
    fade=True,
    default_fade=0.5)

# Character definition
define haru = Character("Haru", color="#ff9999")

# Positioning transforms
transform haru_center:
    xalign 0.5
    yalign 1.0

transform haru_left:
    xalign 0.25
    yalign 1.0

transform haru_right:
    xalign 0.75
    yalign 1.0

# Test label for Haru
label test_haru_live2d:
    scene black
    
    system "=== Haru Live2D Test ==="
    narrator "Testing with the properly configured Haru model."
    
    # Show Haru with default idle animation
    show haru at haru_center
    haru "Hi! I'm Haru, and I should be animated!"
    narrator "Haru is using the default idle animation."
    pause 2.0
    
    # The model has these motion groups defined: Idle, TapBody
    # Motion names from the files: haru_g_idle, haru_g_m01 through haru_g_m26
    
    # Try different motions - names might be normalized
    # Try without prefix first (most likely based on docs)
    show haru g_m01
    haru "Testing motion g_m01..."
    pause 2.0
    
    show haru g_m06
    haru "Testing motion g_m06..."
    pause 2.0
    
    show haru g_m15
    haru "Testing motion g_m15..."
    pause 2.0
    
    show haru g_m20
    haru "Testing motion g_m20..."
    pause 2.0
    
    # Try using expressions (F01 through F08)
    show haru f01
    haru "Testing expression F01..."
    pause 2.0
    
    show haru f02
    haru "Testing expression F02..."
    pause 2.0
    
    show haru f03
    haru "Testing expression F03..."
    pause 2.0
    
    # Combine motion and expression
    show haru g_m10 f04
    haru "Testing motion m10 with expression F04..."
    pause 2.0
    
    # Back to idle - try different variations
    show haru g_idle
    haru "Back to idle animation."
    
    hide haru
    return

# Interactive test for Haru
label test_haru_interactive:
    scene black
    
    system "=== Haru Interactive Test ==="
    
    show haru at haru_center
    haru "Let's test different motions interactively!"
    
    menu haru_motion_menu:
        haru "Which motion would you like to see?"
        
        "Idle":
            show haru g_idle
            haru "This is my idle animation."
            jump haru_motion_menu
            
        "Motion 01":
            show haru g_m01
            haru "Playing motion 01..."
            jump haru_motion_menu
            
        "Motion 06":
            show haru g_m06
            haru "Playing motion 06..."
            jump haru_motion_menu
            
        "Motion 10":
            show haru g_m10
            haru "Playing motion 10..."
            jump haru_motion_menu
            
        "Motion 15":
            show haru g_m15
            haru "Playing motion 15..."
            jump haru_motion_menu
            
        "Motion 20":
            show haru g_m20
            haru "Playing motion 20..."
            jump haru_motion_menu
            
        "Motion 26":
            show haru g_m26
            haru "Playing motion 26..."
            jump haru_motion_menu
            
        "Test Expressions":
            jump haru_expression_menu
            
        "Exit":
            hide haru
            return
    
    label haru_expression_menu:
        menu:
            haru "Which expression?"
            
            "F01":
                show haru f01
                haru "Expression F01"
                jump haru_expression_menu
                
            "F02":
                show haru f02
                haru "Expression F02"
                jump haru_expression_menu
                
            "F03":
                show haru f03
                haru "Expression F03"
                jump haru_expression_menu
                
            "F04":
                show haru f04
                haru "Expression F04"
                jump haru_expression_menu
                
            "F05":
                show haru f05
                haru "Expression F05"
                jump haru_expression_menu
                
            "F06":
                show haru f06
                haru "Expression F06"
                jump haru_expression_menu
                
            "F07":
                show haru f07
                haru "Expression F07"
                jump haru_expression_menu
                
            "F08":
                show haru f08
                haru "Expression F08"
                jump haru_expression_menu
                
            "Back to Motions":
                jump haru_motion_menu

# Demo scene with Haru
label haru_demo_scene:
    scene black
    
    narrator "A day with Haru..."
    
    show haru g_idle at haru_center
    haru "Good morning! Let me show you my expressions and motions!"
    
    show haru g_m03 f01
    haru "I can look happy!" 
    pause 2.0
    
    show haru g_m07 f02
    haru "Or maybe a bit surprised?"
    pause 2.0
    
    show haru g_m10 f03
    haru "Sometimes I'm thoughtful..."
    pause 2.0
    
    show haru g_m20 f04
    haru "And sometimes excited!"
    pause 2.0
    
    show haru g_m26 f05
    haru "I can be energetic too!"
    pause 2.0
    
    show haru g_m15 f06
    haru "Or calm and relaxed."
    pause 2.0
    
    show haru g_idle f07
    haru "Each expression changes how I look!"
    pause 2.0
    
    show haru g_m09 f08
    haru "And motions make me move naturally!"
    pause 2.0
    
    show haru g_idle
    haru "That's all for now. Thanks for watching!"
    
    hide haru
    
    return

# Comparison test between Haru and Ivy
label compare_models:
    scene black
    
    system "=== Model Comparison ==="
    narrator "Let's compare the working Haru model with the static Ivy model."
    
    # Show Ivy (static)
    show ivy neutral at Transform(xalign=0.25, yalign=1.0)
    ivy "I'm Ivy. My model doesn't have motion references, so I'm static."
    
    # Show Haru (animated)
    show haru g_idle at Transform(xalign=0.75, yalign=1.0)
    haru "I'm Haru! My model has proper motion references, so I can move!"
    
    narrator "Notice how Haru has subtle idle animations while Ivy is completely still."
    
    show haru g_m20
    haru "I can change my motion dynamically!"
    
    hide ivy
    show ivy happy at Transform(xalign=0.25, yalign=1.0)
    ivy "I can change images, but I'm still static."
    
    show haru f04
    haru "I can also change expressions!"
    
    narrator "The difference is in the model configuration."
    narrator "Haru.model3.json has a 'Motions' section, Ivy.model3.json doesn't."
    
    hide ivy
    hide haru
    
    return