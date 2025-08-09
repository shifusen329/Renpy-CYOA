# Project Plan: Dynamic CYOA Visual Novel with Ren’Py, Live2D, Ollama, Stable Diffusion WebUI, and OpenAI-compatible TTS

Last updated: 2025-08-09
Status: Planning complete, ready to scaffold

## 1) Overview

We will build a choose-your-own-adventure (CYOA) visual novel using:
- Ren’Py (game engine and UI)
- Live2D Cubism (character rendering and motions)
- Ollama (LLM for planning, narrative, dialog)
- Stable Diffusion WebUI (automatic1111) for backgrounds/CG generation
- OpenAI-compatible TTS endpoint for voice lines

A unified backend exposes:
1) POST /api/generate — generic single-shot text generation
2) POST /api/chat — multi-turn chat (non-OpenAI schema)
3) POST /v1/audio/speech — OpenAI-compatible TTS
4) POST /v1/chat/completions — OpenAI-compatible chat
5) POST /sdapi/v1/txt2img — Stable Diffusion Image Generation

Dynamic scene generation is orchestrated through multiple agents:
- Orchestrator Agent
- Narrative Agent
- Dialog Agent
- Image Prompt Agent
- (Optional) Consistency/Canon Agent

Primary objectives:
- Generate scene plans and dialog lines on the fly from player decisions
- Animate Live2D emotions per line
- Generate and cache backgrounds with SD WebUI
- Play voiced dialog via TTS, with caching
- Keep latency low via prefetching and async pipelines

The project directory is Project/.

## 2) Architecture

High-level components:
- Ren’Py game layer:
  - Scene flow (labels, menus)
  - Live2D displayable and motion control
  - Audio/TTS playback
  - Screens and UX indicators (loading/spinner)
- AI integration layer (Python modules importable in Ren’Py):
  - HTTP client(s) for backend endpoints
  - Agent implementations (orchestrator, narrative, dialog, image prompt)
  - State management and serialization (save-safe)
  - Caching utilities (images/audio)
  - Stable Diffusion WebUI client
  - Live2D emotion mapping bridge

Data flow per user turn:
1) Player selects a choice
2) Orchestrator Agent produces next scene plan (location, beats, emotion trajectory)
3) Parallel:
   - Narrative Agent: scene summary for logs/memory
   - Image Prompt Agent: background prompt → SD WebUI → cached image
4) Dialog Agent returns lines: [{text, emotion, character, voice?, sfx?}, ...]
5) For each line:
   - Live2D emotion/motion update
   - TTS cache lookup → fetch if missing
   - Play audio while rendering text
   - Prefetch TTS for the next line
6) Persist distilled state/memory

Performance/UX strategies:
- Prefetch next TTS while current line plays
- Cache all SD images and TTS by content hash
- Timeouts and retries with graceful fallbacks
- Loading indicators for long operations
- Optional streaming for chat if backend supports SSE

## 3) Directory Structure (under Project/)

- Project/game/                Ren’Py .rpy and Python modules
  - script.rpy                 Scene flow, demo label, integration call points
  - screens.rpy                Loading indicators, debug overlays
  - live2d.rpy                 Live2D displayables/motions/parameters
  - audio_tts.rpy              TTS playback helpers and prefetch
  - ai/
    - __init__.py
    - config.py                Reads API_BASE_URL and API_KEY; flags, model names
    - api.py                   HTTP clients for /api/generate, /api/chat, /v1 endpoints
    - agents.py                Orchestrator/Narrative/Dialog/ImagePrompt agents
    - state.py                 Save-safe state/memory handling
    - sd_client.py             Stable Diffusion WebUI txt2img(img2img optional)
    - live2d_bridge.py         Emotion → Live2D motions/parameters
    - cache.py                 Disk cache (images/audio) by content hash
    - prompts/
      - narrative.txt
      - dialog.txt
      - image_prompt.txt
- Project/game/assets/
  - images/generated/          SD outputs by prompt hash
  - audio/tts/                 TTS files by text hash
  - live2d/                    Optional copy of model files for packaging (e.g., eva/)
- .env                         API_BASE_URL, API_KEY, model/endpoint config

Note: The repository also contains eva/ with model files; for packaging we may relocate or symlink as needed.

## 4) Environment Variables (.env)

- API_BASE_URL                Base URL for our backend proxy (serving endpoints below)
- API_KEY                     Authentication (if required by backend)
- DEFAULT_CHAT_MODEL          e.g., "ollama:llama3.1" or "gpt-4o-mini"
- SD_WEBUI_URL                e.g., "http://127.0.0.1:7860"
- TTS_MODEL                   e.g., "tts-1"
- TTS_VOICE                   e.g., "alloy"
- HTTP_TIMEOUTS               Optional, or split CONNECT_TIMEOUT, READ_TIMEOUT
- FEATURE_FLAGS               Optional, e.g., "enable_streaming=true"

## 5) Backend API Contracts (Recommended Shapes)

Adjust api.py if backend differs. These schemas standardize client code.

1) POST /api/generate — Single-shot text generation
Request:
```json
{
  "model": "ollama:llama3.1",
  "prompt": "You are the Image Prompt Agent... [context]",
  "temperature": 0.7,
  "max_tokens": 512
}
```
Response:
```json
{
  "text": "Generated text here",
  "usage": {"prompt_tokens": 123, "completion_tokens": 456}
}
```

2) POST /api/chat — Multi-turn chat
Request:
```json
{
  "model": "ollama:llama3.1",
  "messages": [
    {"role": "system", "content": "You are the Orchestrator Agent..."},
    {"role": "user", "content": "Player chose: Explore the forest."}
  ],
  "temperature": 0.8,
  "stream": false
}
```
Response (non-stream):
```json
{
  "message": {"role": "assistant", "content": "Proposed scene beats..."},
  "tool_calls": [],
  "usage": {"prompt_tokens": 100, "completion_tokens": 200}
}
```

3) POST /v1/audio/speech — OpenAI-compatible TTS
Request:
```json
{
  "model": "tts-1",
  "voice": "alloy",
  "input": "The line to be spoken.",
  "format": "wav"
}
```
Response (binary or base64 wrapper):
```json
{ "audio": "base64-encoded-audio", "format": "wav" }
```

4) POST /v1/chat/completions — OpenAI-compatible chat
Request:
```json
{
  "model": "gpt-4o-mini",
  "messages": [{ "role": "system", "content": "..." }, ...],
  "temperature": 0.7,
  "tools": []
}
```
Response:
```json
{
  "id": "chatcmpl-...",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Text content",
        "tool_calls": []
      },
      "finish_reason": "stop"
    }
  ],
  "usage": { }
}
```

Stable Diffusion WebUI (automatic1111) — txt2img
- Endpoint: `${SD_WEBUI_URL}/sdapi/v1/txt2img`
- Request:
```json
{
  "prompt": "Cozy forest clearing at dusk, ...",
  "negative_prompt": "lowres, blurry, ...",
  "steps": 28,
  "sampler_name": "Euler a",
  "cfg_scale": 6.5,
  "width": 1024,
  "height": 576,
  "seed": -1
}
```
- Response:
```json
{
  "images": ["base64-..."],
  "parameters": { },
  "info": "..."
}
```

## 6) Agents

- Orchestrator Agent
  - Input: Player choice, current state
  - Output: Scene plan: {location, beats[], required assets, emotion trajectory, npc presence}
- Narrative Agent
  - Input: Orchestrator plan + world/style guide
  - Output: Concise scene summary, pacing notes
- Dialog Agent
  - Input: Plan + summary + character voice/style sheets
  - Output: Array of dialog lines: [{character, text, emotion, tts_voice?}]
- Image Prompt Agent
  - Input: Plan/summary
  - Output: SD prompt, negative prompt, and generation params
- Consistency/Canon Agent (optional)
  - Maintains glossary and style constraints, post-edits for consistency

Prompts live in Project/game/ai/prompts/*.txt, with variable insertion for scene-specific context.

## 7) Ren’Py Integration

- script.rpy:
  - label start initializes state, shows first menu
  - After choice, calls orchestrate_next() to get plan+assets
  - Shows background (cached SD image)
  - Iterates dialog lines: for each line:
    - live2d_bridge.set_emotion(emotion)
    - audio_tts.play_tts(text, voice)
    - renpy.say(character, text)
- live2d.rpy:
  - Defines Live2D displayable for EVA
  - Maps emotion → motion group/name or parameter blend
- audio_tts.rpy:
  - TTS caching and playback helpers
  - Prefetch next line’s audio while current line plays
- screens.rpy:
  - Loading overlays (e.g., while generating background)
  - Debug/log panes if enabled

## 8) Live2D Emotion Mapping

- Example mapping (to be refined based on available motions):
  - happy → motions["IdleHappy_01"]
  - neutral → motions["Idle_01"]
  - sad → motions["IdleSad_01"]
  - angry → motions["IdleAngry_01"]
- live2d_bridge.py surface:
  - set_emotion(emotion: str)
  - speak_line(emotion: str, text: str) [optional helper to orchestrate emotion+tts]

## 9) Stable Diffusion WebUI Integration and Caching

- Compute cache key as SHA256 of:
  prompt + negative_prompt + steps + sampler + cfg + width + height + seed(if fixed)
- Store in Project/game/assets/images/generated/<hash>.png
- Reuse cached image if present; regenerate otherwise
- Fallback background if SD unavailable; retry in background

## 10) TTS Integration and Caching

- Cache key: SHA256(voice_id + text)
- Store in Project/game/assets/audio/tts/<hash>.<ext>
- On playback request:
  1) Check disk cache
  2) If miss, call /v1/audio/speech, store, then play
- Graceful fallback to text-only with subtle SFX on error

## 11) State, Persistence, and Saves

- state.py keeps a compact memory:
  - player_profile (choices, traits)
  - world_facts (location, time, known NPCs)
  - last_scene_summary
  - glossary/canon (optional)
- Provide to_serializable() / from_serializable()
- Ensure data is Ren’Py save/load safe

## 12) Error Handling and Fallbacks

- Centralize HTTP retries/backoff in api.py
- If SD fails: show neutral/local background, log error, retry later
- If TTS fails: play SFX and show text
- If chat/generation fails: show in-fiction “glitch” line, retry once, then branch to safety scene

## 13) Security Considerations

- Do not embed API_KEY in shipped builds
- In dev: load from .env or environment
- For distribution: proxy requests via user-local backend or documented setup
- Keep caches within Project/game/assets; clean-up tooling optional

## 14) Milestones

Milestone 1: Scaffolding and Stubs
- Create ai/ modules (config.py, api.py, agents.py stubs, sd_client.py, live2d_bridge.py, cache.py, state.py)
- Add prompts/ templates (narrative.txt, dialog.txt, image_prompt.txt)
- Add live2d.rpy with EVA idle motion
- Add script.rpy with minimal menu → single line via /api/generate
- Add audio_tts.rpy with local playback of a test file

Milestone 2: Dialog + TTS
- Implement /v1/chat/completions client (optional streaming)
- Implement TTS caching and playback via /v1/audio/speech
- Drive N dialog lines with per-line emotions and Live2D motions

Milestone 3: Background Generation
- Implement image prompt agent + sd_client txt2img
- Cache by prompt hash
- Show SD-generated backgrounds with transitions

Milestone 4: Orchestration and Narrative Planning
- Orchestrator Agent: player choice + state → scene plan
- Narrative Agent: scene summary + pacing notes
- Update state and memory persistence

Milestone 5: Polish and Robustness
- Loading indicators, retries/backoff, configurable timeouts
- Settings screen for model toggles and feature flags
- Export build; verify secrets are excluded

## 15) Acceptance Criteria

- Start game → first choice → dynamic plan → background loaded/generated → 5 dialog lines with TTS and Live2D emotions
- Save mid-conversation → reload resumes seamlessly
- Settings allow disabling SD and TTS; fallback gracefully
- Offline mode: cached assets or fallbacks without crashes
- Logs provide insight into generation and caching decisions

## 16) Risks and Mitigations

- Latency from multiple calls
  - Prefetch TTS; cache aggressively; parallelize image generation
- Model quality variability
  - Iterate prompt templates; add style/canon constraints
- Large assets impacting repo
  - Ensure .gitignore excludes generated assets if desired; consider separate data cache
- Live2D motion availability mismatch
  - Audit EVA motions; build robust emotion→motion mapping with fallbacks

## 17) Immediate Next Steps

- Scaffold Project/game/ tree and ai/ modules
- Implement config.py (env loading) and api.py (HTTP client with timeouts/retries)
- Create prompts/ templates
- live2d.rpy minimal EVA displayable
- script.rpy initial label with one menu and dynamic line retrieval
- audio_tts.rpy TTS cache/playback stub
