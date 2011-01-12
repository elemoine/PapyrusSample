from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from papyrus.renderers import geojson_renderer_factory

from papyrussample.models import initialize_sql

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)
    config.add_renderer('geojson', geojson_renderer_factory)
    config.add_static_view('static', 'papyrussample:static')
    config.add_route('summits_read_many', '/summits', request_method='GET')
    config.add_route('summits_read_one', '/summits/{id}', request_method='GET')
    config.add_route('summits_count', '/summits/count', request_method='GET')
    config.add_route('summits_create', '/summits', request_method='POST')
    config.add_route('summits_update', '/summits/{id}', request_method='PUT')
    config.add_route('summits_delete', '/summits/{id}', request_method='DELETE')
    config.scan()
    return config.make_wsgi_app()


