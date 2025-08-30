We are integrating ren'py with the live2d cubism sdk, ollama, stable-diffusion-webui, and an openai compatible tts endpoint to dynamically generate a choose your own adventure style visual novel.
The unified API_BASE_URL and API_KEY are in the .env file. It serves the following endpoints:
1) /api/generate
2) /api/chat
3) /v1/audio/speech
4) /v1/chat/completions
We'll likely need an orchestrator agent, an image prompt generation agent, a narrative agent, a dialog agent, etc.

The project directory is Project/