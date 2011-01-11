from pyramid.view import view_config

from papyrussample.models import DBSession, Summit
from papyrus.protocol import Protocol

proto = Protocol(DBSession, Summit, Summit.geom, epsg=4326)

@view_config(route_name='summits_read', renderer='geojson')
def read(request):
    return proto.read(request)

@view_config(route_name='summits_count', renderer='string')
def count(request):
    return proto.count(request)

@view_config(route_name='summits_create', renderer='geojson')
def create(request):
    return proto.create(request)

@view_config(route_name='summits_update', renderer='geojson')
def update(request):
    return proto.create(request)

@view_config(route_name='summits_delete')
def delete(request):
    return proto.delete(request)
