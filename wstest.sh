#!/bin/bash

set -e

curl 'http://localhost:5000/countries/1'
curl 'http://localhost:5000/countries/1?no_geom=true'
curl 'http://localhost:5000/countries/1?no_geom=true&attrs=name'
curl 'http://localhost:5000/countries?limit=10&offset=2'
curl 'http://localhost:5000/countries?limit=10&order_by=name&dir=DESC'
curl 'http://localhost:5000/countries?lon=86.86&lat=27.86&tolerance=5'
curl 'http://localhost:5000/countries?bbox=85,26,87,28'
curl 'http://localhost:5000/countries?limit=3&queryable=name,pop2005&name__ilike=A%&pop2005__gte=8352021'
curl 'http://localhost:5000/countries?limit=3&queryable=name,pop2005&name__ilike=A%'
curl 'http://localhost:5000/countries' -X POST -H 'Content-Type:"application/json"' -d '{"type": "FeatureCollection", "features": [{"type": "Feature", "id": 247, "geometry": {"type": "MultiPolygon", "coordinates": [[[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]], [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]], [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]]]}}]}'
curl 'http://localhost:5000/countries/247' -X PUT -H 'Content-Type:"application/json"' -d '{"type": "Feature", "geometry": {"type": "MultiPolygon", "coordinates": [[[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]], [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]], [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]]]}, "properties": {"name": "bar"}}'
curl 'http://localhost:5000/countries/247' -X DELETE
