from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    Numeric
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from geoalchemy import GeometryColumn, Point

from papyrus.geo_interface import GeoInterface

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Country(GeoInterface, Base):
    __tablename__ = 'thematic_mapping_world'
    gid = Column(Integer, primary_key=True)
    name = Column(Unicode(50))
    pop2005 = Column(Numeric)
    the_geom = GeometryColumn('the_geom', Point(srid=4326))
