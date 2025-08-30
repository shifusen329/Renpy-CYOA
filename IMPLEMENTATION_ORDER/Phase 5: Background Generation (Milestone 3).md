## Phase 5: Background Generation (Milestone 3)
**Goal**: Generate and cache SD backgrounds

### Step 5.1: Build SD WebUI Client
- `Project/game/ai/sd_client.py`:
  - txt2img endpoint integration
  - Handle base64 image responses
  - Parameter configuration
  - Error handling for SD unavailable

### Step 5.2: Implement Image Prompt Agent
- Create `prompts/image_prompt.txt`
- Generate SD-optimized prompts
- Include negative prompts
- Style consistency hints

### Step 5.3: Create Image Cache System
- Extend cache.py for images:
  - Cache key: SHA256(full prompt + params)
  - Store in `Project/game/assets/images/generated/`
  - PNG format optimization

### Step 5.4: Integrate Backgrounds in Ren'Py
- `Project/game/backgrounds.rpy`:
  ```renpy
  python:
      def show_generated_bg(prompt):
          bg_path = get_or_generate_background(prompt)
          renpy.scene()
          renpy.show(bg_path)
          renpy.with_statement(dissolve)
  ```

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