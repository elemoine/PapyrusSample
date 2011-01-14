#!/bin/bash

set -e

curl 'http://localhost:5000/summits/1'
curl 'http://localhost:5000/summits/1?no_geom=true'
curl 'http://localhost:5000/summits/1?no_geom=true&attrs=elevation'
curl 'http://localhost:5000/summits?limit=10&offset=2'
curl 'http://localhost:5000/summits?limit=10&order_by=elevation&dir=DESC'
curl 'http://localhost:5000/summits?lon=86.86&lat=27.86&tolerance=5'
curl 'http://localhost:5000/summits?bbox=85,26,87,28'
curl 'http://localhost:5000/summits?limit=3&queryable=name,elevation&name__ilike=%col%&elevation__gte=1800'
curl 'http://localhost:5000/summits?limit=3&queryable=name,elevation&name__ilike=%col%'
curl 'http://localhost:5000/summits' -X POST -H 'Content-Type:"application/json"' -d '{"type": "FeatureCollection", "features": [{"type": "Feature", "id": 1000, "geometry": {"type": "Point", "coordinates": [5.8, 45.3]}}]}'
curl 'http://localhost:5000/summits' -X POST -H 'Content-Type:"application/json"' -d '{"type": "FeatureCollection", "features": [{"type": "Feature", "id": 1000, "geometry": {"type": "Point", "coordinates": [5.8, 45.3]}}]}'
curl 'http://localhost:5000/summits/1000' -X PUT -H 'Content-Type:"application/json"' -d '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [6.0, 46]}, "properties": {"name": "foo", "elevation": 1000}}'
curl 'http://localhost:5000/summits/1000' -X DELETE
