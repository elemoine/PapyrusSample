from pyramid.config import Configurator

import pyramid_beaker
import pyramid_handlers

import pyramid_sqla
from pyramid_sqla.static import add_static_route

import papyrus

import papyrus_tilecache

from papyrussample.renderer import geojson_renderer_factory
from papyrussample.views import MapnikRendererFactory

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
    config.add_renderer('.xml', MapnikRendererFactory)
    config.add_renderer('.css', MapnikRendererFactory)

    config.add_subscriber('papyrussample.subscribers.add_renderer_globals',
                          'pyramid.events.BeforeRender')

    # Plug TileCache in
    config.include(papyrus_tilecache)

    # Set up routes and views
    config.include(pyramid_handlers)
    config.include(papyrus)
    config.add_papyrus_handler('countries', '/countries',
                               'papyrussample.handlers:CountriesHandler')
    config.add_handler('home', '/', 'papyrussample.handlers:MainHandler',
                       action='index')
    config.add_route('countries_mapnik', '/countries.png')
    config.add_handler('main', '/{action}', 'papyrussample.handlers:MainHandler',
        path_info=r'/(?!favicon\.ico|robots\.txt|w3c)')
    add_static_route(config, 'papyrussample', 'static', cache_max_age=3600)

    config.scan()

    return config.make_wsgi_app()
