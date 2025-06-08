from app import app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from asgiref.wsgi import WsgiToAsgi


application = DispatcherMiddleware(None, {
    "/flask_asgi_nginx": app  
})

asgi_app = WsgiToAsgi(application)
