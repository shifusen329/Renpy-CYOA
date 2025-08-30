# Dynamic CYOA Visual Novel - Project Structure

## Main Files

### Core Scripts
- `script.rpy` - Main game script with organized menu system
- `haru_live2d.rpy` - Working Live2D implementation using Haru model
- `haru_test_simple.rpy` - Simple tests for Haru model
- `audio_tts.rpy` - TTS audio system with caching
- `tts_test.rpy` - TTS testing suite

### AI Integration (`ai/` directory)
- `config.py` - Configuration management
- `api.py` - HTTP client with retry logic
- `cache.py` - Content caching system
- `state.py` - Game state management
- `audio_cache.py` - TTS audio caching
- `live2d_bridge.py` - Live2D emotion mapping (for Ivy model)

### Assets
- `assets/live2d/Haru/` - Working Live2D model with animations
- `assets/audio/tts/` - Cached TTS audio files
- `assets/images/generated/` - Generated images (future use)

## Test Files (Archived)

### `tests/live2d_ivy/`
Contains test files for the Ivy model (static, non-working):
- `live2d.rpy` - Original Ivy implementation
- `live2d_test.rpy` - Ivy test scenes
- `live2d_debug.rpy` - Debug configuration

### `tests/live2d_deprecated/`
Contains deprecated Live2D implementations that didn't work:
- `live2d_proper.rpy` - Attempted proper implementation
- `live2d_fixed.rpy` - Separate images approach
- `live2d_working.rpy` - Explicit motion files
- `live2d_simple.rpy` - Simplified test
- `live2d_demo.rpy` - Demo scenes

## How to Use

### Running the Game
```bash
cd /home/administrator/python-share/renpy-8.4.1-sdk
./renpy.sh Project
```

### Menu Structure
1. **Live2D Testing (Haru)** - Working Live2D animations
2. **Live2D Testing (Ivy)** - Static model (for comparison)
3. **TTS Audio Testing** - Text-to-speech with caching
4. **API Testing** - Infrastructure and API tests
5. **System Status** - View implementation status

## Implementation Status

### ✅ Phase 1: Core Infrastructure
- Configuration management
- HTTP client with retries
- Content caching
- State management

### ✅ Phase 2: Live2D Integration
- **Haru Model**: Fully working with animations
- **Ivy Model**: Static (missing motion references in model file)

### ✅ Phase 3: TTS Integration
- Audio caching system
- 6 voice options
- Prefetch mechanism

### 🔄 Phase 4: Agent Framework (Not yet implemented)
### 🔄 Phase 5: Asset Generation Pipeline (Not yet implemented)

## Known Issues

1. **Ivy Model**: Doesn't animate because `Ivy.model3.json` lacks motion references
2. **Display**: Requires display for testing (headless server shows errors but logic works)
3. **API**: Requires backend server to be running for API/TTS features

## Model Comparison

### Haru (Working)
- Has "Motions" section in model3.json
- Animations play correctly
- Expressions work

### Ivy (Static)
- Missing "Motions" section in model3.json
- Displays but doesn't animate
- Would need model file editing or re-export to fix