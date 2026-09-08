# 🔀 Super Router Plugin for Agent Zero

Auto-switch between multiple API keys, providers, and models with intelligent failover and usage tracking.

## Features
- ✅ **Multi-Provider Support** – Google Gemini, Groq, OpenRouter, OpenAI, Anthropic, Mistral
- ✅ **Auto-Failover** – Switches keys when one hits rate limits
- ✅ **Smart Cooldown** – Failed keys get a cooldown period before retry
- ✅ **Usage Tracking** – Least-used keys get priority
- ✅ **Web UI** – Easy key management at `/admin/super_router`

## Installation
1. Open **Settings → Plugins** in Agent Zero
2. Search for "Super Router"
3. Click **Install**

## Configuration
1. Go to `/admin/super_router`
2. Add your API keys with provider and model
3. Click **Save All Keys**

## License
MIT
