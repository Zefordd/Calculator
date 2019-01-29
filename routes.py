from auth.views import Login, Logout, Signup
from main_page.views import Index, Feedback, Spiral, Metronome
from main_page.user_file import User_file

from settings import BaseConfig

def setup_routes(app):
    app.router.add_get('/', Index.get, name='index')

    app.router.add_get('/login', Login.get, name='login')
    app.router.add_post('/login', Login.post)
    app.router.add_get('/logout', Logout.get, name='logout')
    app.router.add_get('/signup', Signup.get, name='signup')
    app.router.add_post('/signup', Signup.post)

    app.router.add_get('/feedback', Feedback.get, name='feedback')
    app.router.add_get('/metronome', Metronome.get, name='metronome')

    app.router.add_post('/save_file', User_file.post, name='save_file')
    app.router.add_post('/spiral', Spiral.post, name='spiral')


def setup_static_routes(app):
    app.router.add_static('/static/', path=BaseConfig.STATIC_DIR, name='static')
