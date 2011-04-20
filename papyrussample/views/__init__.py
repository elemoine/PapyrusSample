import decimal

from pyramid.response import Response

import mapnik2 as mn

from shapely.geometry import asShape

from papyrus.protocol import Protocol

from papyrussample.models import Session, Country

proto = Protocol(Session, Country, 'the_geom')

def renderer():
    # create and populate mapnik memory datasource
    ds = mn.MemoryDatasource()
    for feature in collection.features:
        # create a mapnik geometry
        wkt = asShape(feature.geometry).wkt
        geometry = mn.Geometry2d.from_wkt(wkt)
        # prepare feature properties
        properties = dict(feature.properties)
        for k,v in properties.iteritems():
            if isinstance(v, decimal.Decimal):
                properties[k] = float(v)
            elif isinstance(v, (datetime.date, datetime.datetime)):
                properties[k] = str(v)
        # create mapnik feature
        feature = mn.Feature(feature.id, geometry, **properties)
        # add feature to data source
        ds.add_feature(feature)

def mapnik(request):
    collection = proto.read(request)

    ds = mn.MemoryDatasource()

    for f in collection.features:
        wkt = asShape(f.geometry).wkt
        geometry = mn.Geometry2d.from_wkt(wkt)
        properties = {'name': f.properties['name'],
                      'POP2005': float(f.properties['pop2005'])}
        feature = mn.Feature(f.id, geometry, **properties)
        ds.add_feature(feature)

    mapfile = 'population.xml'
    m = mn.Map(1400, 600)
    mn.load_map(m, mapfile)

    layer = m.layers[0]
    layer.datasource = ds

    m.zoom_to_box(layer.envelope())

    im = mn.Image(m.width,m.height)
    mn.render(m, im, 1, 1)

    resp = Response(im.tostring('png'))
    resp.content_type = 'image/png'
    return resp
