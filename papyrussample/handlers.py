import logging

from pyramid.view import action

from papyrussample.models import Session, Summit
from papyrus.protocol import Protocol

proto = Protocol(Session, Summit, 'geom')

log = logging.getLogger(__name__)

class MainHandler(object):
    def __init__(self, request):
        self.request = request

    @action(renderer='index.html')
    def index(self):
        log.debug("testing logging; entered MainHandler.index()")
        return {'project':'papyrussample'}

class SummitsHandler(object):
    def __init__(self, request):
        self.request = request

    @action(renderer='geojson')
    def read_many(self):
        return proto.read(self.request)

    @action(renderer='geojson')
    def read_one(self):
        id = self.request.matchdict.get('id', None)
        return proto.read(self.request, id=id)

    @action(renderer='string')
    def count(self):
        return proto.count(self.request)

    @action(renderer='geojson')
    def create(self):
        return proto.create(self.request)

    @action(renderer='geojson')
    def update(self):
        id = self.request.matchdict['id']
        return proto.update(self.request, id)

    @action()
    def delete(self):
        id = self.request.matchdict['id']
        return proto.delete(self.request, id)
