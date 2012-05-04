from pyramid.view import view_config

from papyrus.protocol import Protocol

from .models import (
    DBSession,
    Country,
    )

proto = Protocol(DBSession, Country, 'the_geom')


@view_config(route_name='countries_raster',
             renderer='papyrussample:mapnik_mapfiles/population.xml')
@view_config(route_name='countries_vector_read_many', renderer='geojson')
def read_many(request):
    return proto.read(request)


@view_config(route_name='countries_vector_read_one', renderer='geojson')
def read_one(request):
    id = request.matchdict.get('id', None)
    return proto.read(request, id=id)


@view_config(route_name='countries_vector_count', renderer='string')
def count(request):
    return proto.count(request)


@view_config(route_name='countries_vector_create', renderer='geojson')
def create(request):
    return proto.create(request)


@view_config(route_name='countries_vector_update', renderer='geojson')
def update(request):
    id = request.matchdict['id']
    return proto.update(request, id)


@view_config(route_name='countries_vector_delete')
def delete(request):
    id = request.matchdict['id']
    return proto.delete(request, id)
