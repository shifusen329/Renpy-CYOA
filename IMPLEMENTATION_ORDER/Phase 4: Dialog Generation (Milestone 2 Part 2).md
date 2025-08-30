## Phase 4: Dialog Generation (Milestone 2 Part 2)
**Goal**: Generate dynamic dialog with emotions

### Step 4.1: Create Agent Base Class
- `Project/game/ai/agents.py`:
  ```python
  class BaseAgent:
      def __init__(self, client, prompt_template):
          self.client = client
          self.prompt_template = prompt_template
      
      def generate(self, context):
          # Template rendering + API call
          pass
  ```

### Step 4.2: Implement Dialog Agent
- Load prompt from `prompts/dialog.txt`
- Parse response into structured format:
  ```python
  [{
      "character": "Ivy",
      "text": "Hello, traveler!",
      "emotion": "happy",
      "voice": "alloy"
  }]
  ```

### Step 4.3: Create Dialog Test Scene
- `Project/game/test_dialog.rpy`:
  - Generate 5 lines based on simple context
  - Play each with TTS and Live2D emotions
  - Test emotion transitions

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