from pyramid.config import Configurator
import pyramid_beaker

import sqlalchemy as sa
import sqlahelper

import papyrus
import papyrus_tilecache
from papyrus_mapnik.renderers import MapnikRendererFactory

from papyrussample.renderer import geojson_renderer_factory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Initialize database
    engine = sa.engine_from_config(settings, prefix='sqlalchemy.')
    sqlahelper.add_engine(engine)

    # Configure Beaker sessions
    session_factory = pyramid_beaker.session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    # Configure renderers
    config.add_renderer('.html', 'pyramid.mako_templating.renderer_factory')
    config.add_renderer('geojson', geojson_renderer_factory)
    config.add_renderer('.xml', MapnikRendererFactory)
    config.add_renderer('.css', MapnikRendererFactory)

    # Plug TileCache in
    config.include(papyrus_tilecache)

    # Set up routes and views
    config.include(papyrus)
    config.add_papyrus_routes('countries_vector', '/countries')
    config.add_route('countries_raster', '/countries.png')
    config.scan()

    return config.make_wsgi_app()
