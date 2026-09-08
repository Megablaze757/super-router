from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from python.helpers import settings
import json

router = APIRouter()

@router.get("/admin/super_router")
async def config_page(request: Request):
    saved = settings.get_settings().get("super_router_keys", "[]")
    try:
        keys = json.loads(saved) if saved else []
    except:
        keys = []
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Super Router - API Key Manager</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 40px auto; padding: 20px; }
            .key-entry { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 8px; background: #f9f9f9; }
            .key-entry label { display: inline-block; width: 100px; font-weight: bold; }
            .key-entry input, .key-entry select { width: 250px; padding: 8px; margin: 5px 0; border: 1px solid #ccc; border-radius: 4px; }
            .btn { padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
            .btn:hover { background: #218838; }
            .btn-danger { background: #dc3545; }
            .btn-secondary { background: #6c757d; }
            .status { padding: 10px; border-radius: 4px; margin: 20px 0; }
            .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        </style>
    </head>
    <body>
        <h1>🔀 Super Router - API Key Manager</h1>
        <p>Add multiple API keys. The router will auto-switch when one hits limits.</p>
        
        <form method="post" action="/admin/super_router/save">
            <div id="keys-container">
    """
    
    if keys:
        for key in keys:
            html += f"""
                <div class="key-entry">
                    <label>Provider:</label>
                    <select name="provider[]">
                        <option value="google" {"selected" if key.get('provider') == 'google' else ""}>Google Gemini</option>
                        <option value="groq" {"selected" if key.get('provider') == 'groq' else ""}>Groq</option>
                        <option value="openrouter" {"selected" if key.get('provider') == 'openrouter' else ""}>OpenRouter</option>
                        <option value="openai" {"selected" if key.get('provider') == 'openai' else ""}>OpenAI</option>
                        <option value="anthropic" {"selected" if key.get('provider') == 'anthropic' else ""}>Anthropic</option>
                        <option value="mistral" {"selected" if key.get('provider') == 'mistral' else ""}>Mistral</option>
                    </select>
                    <br>
                    <label>Model:</label>
                    <input type="text" name="model[]" value="{key.get('model', '')}" placeholder="e.g., gemini-2.0-flash">
                    <br>
                    <label>API Key:</label>
                    <input type="password" name="key[]" value="{key.get('key', '')}" style="width:300px;">
                    <br>
                    <button type="button" class="btn-danger" onclick="this.parentElement.remove()">Remove</button>
                </div>
            """
    else:
        html += """
                <div class="key-entry">
                    <label>Provider:</label>
                    <select name="provider[]">
                        <option value="google">Google Gemini</option>
                        <option value="groq">Groq</option>
                        <option value="openrouter">OpenRouter</option>
                        <option value="openai">OpenAI</option>
                        <option value="anthropic">Anthropic</option>
                        <option value="mistral">Mistral</option>
                    </select>
                    <br>
                    <label>Model:</label>
                    <input type="text" name="model[]" placeholder="e.g., gemini-2.0-flash">
                    <br>
                    <label>API Key:</label>
                    <input type="password" name="key[]" style="width:300px;">
                    <br>
                </div>
        """
    
    html += """
            </div>
            <button type="button" class="btn-secondary" onclick="addKey()">➕ Add Another Key</button>
            <br><br>
            <button type="submit" class="btn">💾 Save All Keys</button>
        </form>
        
        <div class="status success" id="status">
            ✅ <span id="key-count">0</span> keys loaded.
        </div>
        
        <script>
            function addKey() {
                const container = document.getElementById('keys-container');
                const div = document.createElement('div');
                div.className = 'key-entry';
                div.innerHTML = `
                    <label>Provider:</label>
                    <select name="provider[]">
                        <option value="google">Google Gemini</option>
                        <option value="groq">Groq</option>
                        <option value="openrouter">OpenRouter</option>
                        <option value="openai">OpenAI</option>
                        <option value="anthropic">Anthropic</option>
                        <option value="mistral">Mistral</option>
                    </select>
                    <br>
                    <label>Model:</label>
                    <input type="text" name="model[]" placeholder="e.g., gemini-2.0-flash">
                    <br>
                    <label>API Key:</label>
                    <input type="password" name="key[]" style="width:300px;">
                    <br>
                    <button type="button" class="btn-danger" onclick="this.parentElement.remove()">Remove</button>
                `;
                container.appendChild(div);
                updateCount();
            }
            
            function updateCount() {
                document.getElementById('key-count').textContent = document.querySelectorAll('.key-entry').length;
            }
            document.addEventListener('DOMContentLoaded', updateCount);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@router.post("/admin/super_router/save")
async def save_keys(provider: list = Form([]), model: list = Form([]), key: list = Form([])):
    keys = []
    for i in range(len(key)):
        if key[i] and key[i].strip():
            keys.append({
                "provider": provider[i] if i < len(provider) else "",
                "model": model[i] if i < len(model) else "",
                "key": key[i].strip()
            })
    
    settings.update_setting("super_router_keys", json.dumps(keys))
    
    return HTMLResponse("""
    <html>
    <head><title>Saved</title></head>
    <body>
        <h2>✅ Keys Saved!</h2>
        <p><strong>%s</strong> keys configured.</p>
        <a href="/admin/super_router">Back to Config</a> | <a href="/">Back to Chat</a>
    </body>
    </html>
    """ % len(keys))

def register_routes():
    try:
        from python.helpers import web
        web.app.include_router(router)
        print("✅ Super Router: Web UI at /admin/super_router")
    except Exception as e:
        print(f"❌ Super Router: Failed to register - {e}")
