import logging

import pyramid_sqla as psa
import sqlalchemy as sa
import sqlalchemy.orm as orm
import transaction

from geoalchemy import GeometryColumn, Point, WKBSpatialElement

import geojson

from shapely.geometry import asShape
from shapely.wkb import loads

log = logging.getLogger(__name__)

Base = psa.get_base()
Session = psa.get_session()

class Summit(Base):
    __tablename__ = 'sommets_out'
    sommet_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Unicode(100))
    elevation = sa.Column(sa.Integer)
    geom = GeometryColumn('geom', Point(srid=4326))

    def __init__(self, feature):
        self.sommet_id = feature.id
        self.__update__(feature)

    def __update__(self, feature):
        geometry = feature.geometry
        if geometry is not None and \
           not isinstance(geometry, geojson.geometry.Default):
            shape = asShape(feature.geometry)
            self.geom = WKBSpatialElement(buffer(shape.wkb), srid=4326)
            self.geom.shape = shape
        self.name = feature.properties.get('name', None)
        self.elevation = feature.properties.get('elevation', None)

    @property
    def __geo_interface__(self):
        id = self.sommet_id
        geometry = loads(str(self.geom.geom_wkb))
        properties = dict(name=self.name, elevation=self.elevation)
        return geojson.Feature(id=id, geometry=geometry, properties=properties)
