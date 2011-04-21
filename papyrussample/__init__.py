from pyramid.config import Configurator

import pyramid_beaker

import pyramid_sqla

import papyrus

import papyrus_tilecache
from papyrus_mapnik.renderers import MapnikRendererFactory

from papyrussample.renderer import geojson_renderer_factory

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
    config.include(papyrus)
    config.add_papyrus_routes('countries_vector', '/countries')
    config.add_route('countries_raster', '/countries.png')
    config.scan()

    return config.make_wsgi_app()
