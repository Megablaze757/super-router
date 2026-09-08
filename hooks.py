import json
import time
from python.helpers import settings

class SuperRouterHooks:
    def __init__(self):
        self.keys = []
        self.current_index = 0
        self.failed_keys = {}
        self.usage_stats = {}
        self.load_keys()

    def load_keys(self):
        saved = settings.get_settings().get("super_router_keys", "[]")
        try:
            self.keys = json.loads(saved) if saved else []
        except:
            self.keys = []
        return self.keys

    def save_keys(self, keys):
        settings.update_setting("super_router_keys", json.dumps(keys))
        self.keys = keys

    def get_best_key(self):
        if not self.keys:
            return None
        
        available = []
        for key_entry in self.keys:
            key_id = key_entry.get("key", "")[:8]
            if key_id in self.failed_keys:
                if time.time() < self.failed_keys[key_id]:
                    continue
                else:
                    del self.failed_keys[key_id]
            
            usage = self.usage_stats.get(key_id, 0)
            available.append((usage, key_entry))
        
        if not available:
            return None
        
        available.sort(key=lambda x: x[0])
        return available[0][1]

    async def before_main_llm_call(self, messages, model_config, request_params):
        self.load_keys()
        
        if not self.keys:
            return messages, model_config, request_params
        
        key_entry = self.get_best_key()
        
        if not key_entry:
            if self.failed_keys:
                min_wait = min(self.failed_keys.values()) - time.time()
                if min_wait > 0:
                    time.sleep(min_wait + 1)
            return messages, model_config, request_params
        
        api_key = key_entry.get("key", "").strip()
        provider = key_entry.get("provider", "").lower()
        model = key_entry.get("model", "")
        
        if api_key:
            request_params["api_key"] = api_key
            
            provider_map = {
                "google": "google",
                "gemini": "google",
                "groq": "groq",
                "openrouter": "openrouter",
                "openai": "openai",
                "anthropic": "anthropic",
                "mistral": "mistral"
            }
            
            request_params["provider"] = provider_map.get(provider, provider)
            
            if model:
                model_config["model"] = model
            
            key_id = api_key[:8]
            self.usage_stats[key_id] = self.usage_stats.get(key_id, 0) + 1
            
            print(f"🔀 Super Router: Using {provider} | {model} | Key: ...{api_key[-4:]}")
            
            return messages, model_config, request_params
        
        return messages, model_config, request_params

    async def after_llm_call(self, response, request_params):
        api_key = request_params.get("api_key", "")
        
        is_error = False
        if hasattr(response, 'error') and response.error:
            is_error = True
        elif hasattr(response, 'status_code') and response.status_code >= 400:
            is_error = True
        
        if is_error and api_key:
            key_id = api_key[:8]
            cooldown = 60
            if key_id in self.failed_keys:
                cooldown = 120
            self.failed_keys[key_id] = time.time() + cooldown
            print(f"⚠️ Super Router: Key {key_id} failed, cooldown {cooldown}s")
        
        return response
