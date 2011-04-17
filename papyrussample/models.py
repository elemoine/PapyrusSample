import logging

import pyramid_sqla as psa
import sqlalchemy as sa
import sqlalchemy.orm as orm
import transaction

from geoalchemy import GeometryColumn, Point

from papyrus.geo_interface import GeoInterface

log = logging.getLogger(__name__)

Base = psa.get_base()
Session = psa.get_session()

class Summit(GeoInterface, Base):
    __tablename__ = 'thematic_mapping_world'
    gid = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Unicode(50))
    pop2005 = sa.Column(sa.Numeric)
    the_geom = GeometryColumn('the_geom', Point(srid=4326))
