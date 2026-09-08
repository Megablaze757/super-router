from .hooks import SuperRouterHooks
from .webui.routes import register_routes

def register_plugin():
    hooks = SuperRouterHooks()
    register_routes()
    return hooks
