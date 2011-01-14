from pyramid.config import Configurator
import pyramid_beaker
import pyramid_sqla
from pyramid_sqla.static import add_static_route

from papyrus.renderers import geojson_renderer_factory

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

    # Set up routes and views
    config.add_handler('summits_read_many', '/summits',
                       'papyrussample.handlers:SummitsHandler',
                       action='read_many', request_method='GET')
    config.add_handler('summits_read_one', '/summits/{id}',
                       'papyrussample.handlers:SummitsHandler',
                       action='read_one', request_method='GET')
    config.add_handler('summits_count', '/summits/count',
                       'papyrussample.handlers:SummitsHandler',
                       action='count', request_method='GET')
    config.add_handler('summits_create', '/summits',
                       'papyrussample.handlers:SummitsHandler',
                       action='create', request_method='POST')
    config.add_handler('summits_update', '/summits/{id}',
                       'papyrussample.handlers:SummitsHandler',
                       action='update', request_method='PUT')
    config.add_handler('summits_delete', '/summits/{id}',
                       'papyrussample.handlers:SummitsHandler',
                       action='delete', request_method='DELETE')
    config.add_handler('home', '/', 'papyrussample.handlers:MainHandler',
                       action='index')
    config.add_handler('main', '/{action}', 'papyrussample.handlers:MainHandler',
        path_info=r'/(?!favicon\.ico|robots\.txt|w3c)')
    add_static_route(config, 'papyrussample', 'static', cache_max_age=3600)

    return config.make_wsgi_app()
