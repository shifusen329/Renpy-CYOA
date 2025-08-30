
## Phase 3: TTS Integration (Milestone 2 Part 1)
**Goal**: Implement voice synthesis with caching

### Step 3.1: Build TTS Client
- Extend `api.py` with TTS-specific methods:
  - `generate_tts(text, voice, model)`
  - Handle binary audio responses
  - Convert formats if needed (base64 → binary)

### Step 3.2: Create Audio Cache System
- `Project/game/ai/audio_cache.py`:
  - Generate cache keys: SHA256(voice + text)
  - Store in `Project/game/assets/audio/tts/`
  - Methods: `get_tts_cached()`, `cache_tts()`

### Step 3.3: Implement Ren'Py Audio Helpers
- `Project/game/audio_tts.rpy`:
  ```renpy
  init python:
      def play_tts_line(text, voice="alloy"):
          audio_path = get_or_generate_tts(text, voice)
          if audio_path:
              renpy.music.play(audio_path, channel="voice")
  ```

### Step 3.4: Create TTS Test Scene
- Generate and play sample lines
- Test caching behavior
- Implement prefetch mechanism

## Testing Checkpoints

After each phase, verify:
- [ ] No runtime errors
- [ ] Features work as expected
- [ ] Performance is acceptable
- [ ] Code is maintainable
- [ ] User experience is smooth

## Risk Mitigation Priorities

1. **API Latency**: Implement aggressive caching first
2. **Model Quality**: Start with simple prompts, iterate
3. **Asset Size**: Use .gitignore early, monitor repo size
4. **Live2D Compatibility**: Test motions early, have fallbacks

## Notes

- Each phase builds on the previous
- Phases 2-5 can be developed in parallel by different developers
- Keep commits atomic and well-documented
- Run tests after each major step
- Document any deviations from the plan