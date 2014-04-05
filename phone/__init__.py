from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)

    config.include('pyramid_jinja2')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')

    config.scan()

    config.include('apex', route_prefix='/auth')
    return config.make_wsgi_app()
