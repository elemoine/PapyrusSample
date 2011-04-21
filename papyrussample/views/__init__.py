from pyramid.response import Response
from pyramid.view import view_config

from papyrus.protocol import Protocol

from papyrussample.models import Session, Country

proto = Protocol(Session, Country, 'the_geom')

@view_config(route_name='countries_mapnik',
             renderer='papyrussample:mapnik_mapfiles/population.xml')
def countries(request):
    return ('countries', proto.read(request))
