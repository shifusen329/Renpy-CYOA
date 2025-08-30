## Phase 6: Orchestration System (Milestone 4)
**Goal**: Implement scene planning and narrative generation

### Step 6.1: Create Orchestrator Agent
- Process player choices into scene plans
- Output structure:
  ```python
  {
      "location": "forest_clearing",
      "beats": ["discovery", "encounter", "choice"],
      "emotion_arc": ["curious", "surprised", "thoughtful"],
      "npcs": ["mysterious_figure"]
  }
  ```

### Step 6.2: Implement Narrative Agent
- Generate scene summaries
- Maintain consistency with world state
- Produce memory-friendly descriptions

### Step 6.3: Build Scene Generation Pipeline
- `Project/game/ai/scene_generator.py`:
  1. Player choice → Orchestrator
  2. Scene plan → Narrative Agent
  3. Summary → Dialog Agent
  4. Plan → Image Prompt Agent
  5. Coordinate parallel generation

### Step 6.4: Create Full Integration Test
- Complete scene with:
  - Player choice
  - Generated background
  - 5-7 dialog lines with emotions
  - TTS playback
  - State updates

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