
## Phase 7: Game Flow & UX (Milestone 5 Part 1)
**Goal**: Build the actual game experience

### Step 7.1: Create Main Game Loop
- `Project/game/script.rpy`:
  - Opening scene
  - Choice menus
  - Scene generation calls
  - State persistence

### Step 7.2: Implement Loading Indicators
- `Project/game/screens.rpy`:
  - Generation spinner overlay
  - Progress text for long operations
  - Smooth transitions

### Step 7.3: Add Prefetching Pipeline
- Prefetch next TTS while current plays
- Pregenerate likely next scenes
- Background loading during dialog

### Step 7.4: Create Save/Load Integration
- Hook state.py into Ren'Py save system
- Test save mid-scene
- Verify reload consistency

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