from pyramid.config import Configurator
from sqlalchemy import engine_from_config

import papyrus
from papyrus.renderers import GeoJSON
from papyrus_mapnik.renderers import MapnikRendererFactory

from .models import DBSession


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.include(papyrus)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_renderer('geojson', GeoJSON())
    config.add_renderer('.xml', MapnikRendererFactory)
    config.add_renderer('.css', MapnikRendererFactory)
    config.add_papyrus_routes('countries_vector', '/countries')
    config.add_route('countries_raster', '/countries.png')
    config.scan()
    return config.make_wsgi_app()
