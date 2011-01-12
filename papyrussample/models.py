import transaction

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

#from zope.sqlalchemy import ZopeTransactionExtension

from geoalchemy import GeometryColumn, Point, WKBSpatialElement

import geojson

from shapely.geometry import asShape
from shapely.wkb import loads

#DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
DBSession = scoped_session(sessionmaker())
Base = declarative_base()

class Summit(Base):
    __tablename__ = 'sommets_out'
    sommet_id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    elevation = Column(Integer)
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
    
def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
