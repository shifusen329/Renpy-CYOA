# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a dynamic CYOA visual novel integrating:
- Ren'Py 8.4.1 SDK as the game engine
- Live2D Cubism SDK for character animations (Ivy model located in Ivy/)
- Ollama LLM for narrative and dialog generation
- Stable Diffusion WebUI for background generation
- OpenAI-compatible TTS for voice synthesis

## Essential Commands

### Running the Game
```bash
# Launch Ren'Py with the Project directory
./renpy.sh Project

# Launch Ren'Py launcher (for project management)
./renpy.sh

# Test specific game projects
./renpy.sh the_question  # Test with example game
./renpy.sh tutorial      # Test with tutorial game
```

### Development Commands
```bash
# Clean compiled files
find Project/game -name "*.rpyc" -delete
find Project/game -name "*.rpyb" -delete

# Check Python syntax in .rpy files
python -m py_compile Project/game/ai/*.py

# Run with console enabled (for debugging)
./renpy.sh Project --args --console
```

## Architecture and Integration Points

### Project Structure
The main game development happens in `Project/` directory:
- `Project/game/` - All Ren'Py scripts and Python modules
- `Project/game/ai/` - AI integration layer (agents, API clients, caching)
- `Project/game/assets/` - Generated and cached assets
- `Ivy/` - Live2D model files (Ivy.model3.json, motions, textures)

### AI Backend Integration
The unified backend (configured in `.env`) provides:
1. `/api/generate` - Single-shot text generation
2. `/api/chat` - Multi-turn chat (non-OpenAI schema)
3. `/v1/audio/speech` - OpenAI-compatible TTS
4. `/v1/chat/completions` - OpenAI-compatible chat
5. `/sdapi/v1/txt2img` - Stable Diffusion image generation (via SD_WEBUI_URL in .env)

### Agent Architecture
The system uses multiple specialized agents:
- **Orchestrator Agent**: Plans scenes based on player choices
- **Narrative Agent**: Generates scene summaries
- **Dialog Agent**: Creates character dialog with emotions
- **Image Prompt Agent**: Generates SD prompts for backgrounds

### Live2D Integration
- Model: `Ivy/Ivy.model3.json`
- Motions: `Ivy/motion/*.motion3.json`
- Integration: `Project/game/ai/live2d_bridge.py` maps emotions to motions
- Ren'Py: `Project/game/live2d.rpy` handles displayable and motion control

### Caching Strategy
- Images: `Project/game/assets/images/generated/` (SHA256 of prompt)
- Audio: `Project/game/assets/audio/tts/` (SHA256 of text+voice)
- Both use content-based hashing for deduplication

### State Management
- `Project/game/ai/state.py` maintains save-compatible game state
- Includes: player choices, world facts, scene summaries
- Must be serializable for Ren'Py's save system

## Critical Implementation Notes

### When modifying AI integration:
1. All HTTP calls go through `Project/game/ai/api.py` with retry logic
2. Agent prompts are in `Project/game/ai/prompts/*.txt`
3. Always check cache before generating new content
4. Use prefetching for TTS while current line plays

### When working with Live2D:
1. Available motions are in `Ivy/motion/`
2. Emotion mapping defined in `live2d_bridge.py`
3. Test with idle motions first before complex animations

### When adding new features:
1. Follow existing patterns in `the_question/` or `tutorial/` examples
2. Test with `./renpy.sh Project --args --console` for debugging
3. Keep generated assets out of git (check `.gitignore`)

## Project Plan References
See `PROJECTPLAN.md` for detailed milestones and implementation steps.
See `PROJECT.MD` for high-level project goals.

## Environment Configuration
Required in `.env`:
- `API_BASE_URL` - Backend proxy URL
- `API_KEY` - Authentication key
- `SD_WEBUI_URL` - Stable Diffusion WebUI URL (if separate)