from .common import *

INSTALLED_APPS = ["debug_toolbar",] + INSTALLED_APPS

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware",] + MIDDLEWARE

INTERNAL_IPS = [
    "127.0.0.1",
]
