<html>
 <head>
     <title>PapyrusSample Application</title>
     <script src="http://openlayers.org/api/2.12-rc2/OpenLayers.light.debug.js"></script>
     <script>
     function init() {

     OpenLayers.Layer.PapyrusMapnik = OpenLayers.Class(OpenLayers.Layer.Grid, {
         getURL: function(bounds) {
                bounds = this.adjustBounds(bounds).toArray();
                var imgSize = this.getImageSize();
                var params = {
                    'bbox': bounds,
                    'img_bbox': bounds,
                    'img_width': imgSize.w,
                    'img_height': imgSize.h
                };
                return this.getFullRequestString(params);
            },
            CLASS_NAME: 'OpenLayers.Layer.PapyrusMapnik'
        });

        var map = new OpenLayers.Map('map', {
            layers: [
                new OpenLayers.Layer.PapyrusMapnik(
                    'papyrus',
                    '${request.route_path('countries_raster')}',
                    {queryable: 'pop2005', 'pop2005__gte': 10000000},
                    {isBaseLayer: true, singleTile: false}
                )
            ],
            center: [0, 0],
            zoom: 3
        });

     }
     </script>
 </head>
   <body onload="init()">
      <h1 class="title">PapyrusSample</h1>
      <div id="map"></div>
   </body>
 </html>
