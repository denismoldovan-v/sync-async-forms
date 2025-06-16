from asgiref.wsgi import WsgiToAsgi
from app import app  
from werkzeug.middleware.dispatcher import DispatcherMiddleware

wsgi_app = DispatcherMiddleware(None, {
	"/flask_asgi_nginx":app
})

application = WsgiToAsgi(wsgi_app)
