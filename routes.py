from auth.views import Login, Logout
from calculator.views import Index, Feedback

from settings import BaseConfig

def setup_routes(app):
    app.router.add_get('/', Index.get, name='index')

    app.router.add_get('/login', Login.get, name='login')
    app.router.add_post('/login', Login.post)
    app.router.add_get('/logout', Logout.get, name='logout')
    app.router.add_get('/feedback', Feedback.get, name='feedback')


def setup_static_routes(app):
    app.router.add_static('/static/', path=BaseConfig.STATIC_DIR, name='static')




    
