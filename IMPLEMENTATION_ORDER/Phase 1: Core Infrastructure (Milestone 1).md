## Phase 1: Core Infrastructure (Milestone 1)
**Goal**: Build foundation modules and basic integration

### Step 1.1: Create Python AI Module Structure
```
Project/game/ai/
├── __init__.py
├── config.py         # Environment variable loading
├── api.py           # HTTP client with retry logic
├── cache.py         # Content-based caching utilities
├── state.py         # Save-compatible state management
└── prompts/         # Agent prompt templates
    └── __init__.py
```

### Step 1.2: Implement Configuration Module
- `config.py`:
  - Load from `.env` using python-dotenv
  - Define configuration dataclass
  - Provide defaults and validation
  - Export: `get_config()` function

### Step 1.3: Build HTTP Client Foundation
- `api.py`:
  - Base HTTP client class with retry/backoff
  - Connection pooling with requests.Session
  - Timeout handling (connect + read)
  - Error wrapping and logging
  - Methods: `post_json()`, `get()`, `post_binary()`

### Step 1.4: Implement Cache System
- `cache.py`:
  - SHA256-based content hashing
  - Directory structure: `type/hash[:2]/hash.ext`
  - Methods: `cache_exists()`, `get_cached()`, `save_to_cache()`
  - Cleanup utilities for old entries

### Step 1.5: Create State Management
- `state.py`:
  - Define GameState class (serializable)
  - Player choices history
  - World facts dictionary
  - Scene summaries list
  - Methods: `to_dict()`, `from_dict()`, `update()`

### Step 1.6: Basic Ren'Py Integration
- `Project/game/script.rpy`:
  ```renpy
  init python:
      import sys
      sys.path.append("game/ai")
      from config import get_config
      from api import APIClient
  
  label start:
      $ config = get_config()
      "Testing configuration: [config.api_base_url]"
      return
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