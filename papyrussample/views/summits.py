from pyramid.view import view_config

from papyrussample.models import DBSession, Summit
from papyrus.protocol import Protocol

proto = Protocol(DBSession, Summit, 'geom')

@view_config(route_name='summits_read_many', renderer='geojson')
def read_many(request):
    return proto.read(request)

@view_config(route_name='summits_read_one', renderer='geojson')
def read_one(request):
    id = request.matchdict.get('id', None)
    return proto.read(request, id=id)

@view_config(route_name='summits_count', renderer='string')
def count(request):
    return proto.count(request)

@view_config(route_name='summits_create', renderer='geojson')
def create(request):
    return proto.create(request)

@view_config(route_name='summits_update', renderer='geojson')
def update(request):
    id = request.matchdict['id']
    return proto.update(request, id)

@view_config(route_name='summits_delete')
def delete(request):
    id = request.matchdict['id']
    return proto.delete(request, id)
