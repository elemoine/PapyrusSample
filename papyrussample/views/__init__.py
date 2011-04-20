import decimal

from pyramid.response import Response
from pyramid.view import view_config

import mapnik2 as mn

from shapely.geometry import asShape

from papyrus.protocol import Protocol

from papyrussample.models import Session, Country

proto = Protocol(Session, Country, 'the_geom')

from pyramid.asset import abspath_from_asset_spec
from pyramid.httpexceptions import HTTPBadRequest
import datetime

class MapnikRendererFactory:
    def __init__(self, info):
        self.mapfile = abspath_from_asset_spec(info.name)

    def _feature_coll_to_datasource(self, collection):
        ds = mn.MemoryDatasource()
        for feature in collection.features:
            wkt = asShape(feature.geometry).wkt
            geometry = mn.Geometry2d.from_wkt(wkt)
            properties = dict(feature.properties)
            for k,v in properties.iteritems():
                if isinstance(v, decimal.Decimal):
                    properties[k] = float(v)
                elif isinstance(v, (datetime.date, datetime.datetime)):
                    properties[k] = str(v)
            ds.add_feature(mn.Feature(feature.id, geometry, **properties))
        return ds

    def _set_layer_in_map(self, m, name):
        layer = None
        for i, l in enumerate(m.layers):
            if l.name != name:
                del m.layers[i]
            else:
                layer = l
        return layer
    
    def __call__(self, value, system):
        request = system['request']

        if not isinstance(value, tuple):
            raise ValueError('renderer is not passed a tuple')

        layer_name, collection = value

        if not hasattr(collection, 'features'):
            raise ValueError('renderer is not passed a feature collection')

        # get image width and height
        try:
            width = int(request.params.get('width', 600))
        except:
            request.response_status = 400
            return 'incorrect width'
        try:
            height = int(request.params.get('height', 400))
        except:
            request.response_status = 400
            return 'incorrect height'

        # get map envelope
        envelope = request.params.get('envelope')
        if envelope:
            try:
                envelope = map(float, envelope.split(','))
            except ValueError:
                request.response_status = 400
                return 'incorrect envelope'
            envelope = mn.Box2d(*envelope)

        m = mn.Map(width, height)
        mn.load_map(m, self.mapfile)

        layer = self._set_layer_in_map(m, layer_name)
        layer.datasource = self._feature_coll_to_datasource(collection)

        m.zoom_to_box(envelope or layer.envelope())

        im = mn.Image(width, height)
        mn.render(m, im, 1, 1)

        system['request'].response_content_type = 'image/png'
        return im.tostring('png')

@view_config(route_name='countries_mapnik',
             renderer='papyrussample:mapnik_mapfiles/population.xml')
def countries(request):
    return ('countries', proto.read(request))
