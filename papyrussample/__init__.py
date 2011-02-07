from pyramid.config import Configurator

import pyramid_beaker

import pyramid_sqla
from pyramid_sqla.static import add_static_route

import papyrus
from papyrus.renderers import geojson_renderer_factory

import papyrus_tilecache

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Initialize database
    pyramid_sqla.add_engine(settings, prefix='sqlalchemy.')

    # Configure Beaker sessions
    session_factory = pyramid_beaker.session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    # Configure renderers
    config.add_renderer('.html', 'pyramid.mako_templating.renderer_factory')
    config.add_renderer('geojson', geojson_renderer_factory)

    config.add_subscriber('papyrussample.subscribers.add_renderer_globals',
                          'pyramid.events.BeforeRender')

    # Plug TileCache in
    config.include(papyrus_tilecache)

    # Set up routes and views
    config.include(papyrus)
    config.add_papyrus_handler('summits', '/summits',
                               'papyrussample.handlers:SummitsHandler')
    config.add_handler('home', '/', 'papyrussample.handlers:MainHandler',
                       action='index')
    config.add_handler('main', '/{action}', 'papyrussample.handlers:MainHandler',
        path_info=r'/(?!favicon\.ico|robots\.txt|w3c)')
    add_static_route(config, 'papyrussample', 'static', cache_max_age=3600)

    return config.make_wsgi_app()
